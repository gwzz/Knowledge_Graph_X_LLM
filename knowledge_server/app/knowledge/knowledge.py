import re
import json
import os
import dotenv
from configs import *
from json_repair import repair_json
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Document,VectorStoreIndex
from llama_index.core.schema import MetadataMode
from llama_index.core.storage import StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
import qdrant_client
import psycopg2
from llama_index.vector_stores.qdrant import QdrantVectorStore
from sqlalchemy.orm import Session
import app.knowledge.knowledge_crud as crud
import app.knowledge.knowledge_schemas as schemas
import app.knowledge.knowledge_models as models
from databases import engine, get_db
import pandas as pd
import time
import schedule
from threading import Thread
from fastapi import Depends
import requests
from utils import get_logging
logger = get_logging(__file__)

dotenv.load_dotenv()
# Load embedding and reranker environment variables

class ContentQuery:
    def __init__(self) -> None:
        self.llm = OpenAILike(
            model=MODEL_NAME,
            api_base=LLM_API_BASE,
            # messages_to_prompt=messages_to_prompt,
            # completion_to_prompt=completion_to_prompt,
            api_key='EMPTY',
            is_chat_model=True,
            temperature=0.6,
            max_tokens=MAX_TOKENS,
            timeout=TIME_OUT,
            additional_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        )

        self.embed_model = OpenAIEmbedding(
            model_name=EMBEDDING_MODEL_NAME,
            api_base=EMBED_API_BASE,
            api_key='EMPTY')
        
        self.rerank_model = OpenAILike(
            model=RERANK_MODEL_NAME,
            api_base=RERANK_API_BASE,
            api_key='EMPTY')

        self.pg_vector_store = PGVectorStore.from_params(
            database='hospital_standards',
            host=POSTGRES_HOST,
            password=POSTGRES_PASSWD,
            port=5432,
            user=POSTGRES_USER_NAME,
            schema_name=POSTGRES_SCHEMA,
            table_name=DIAGNOSIS_STANDARD_TABLE_NAME,
            embed_dim=1024,
            hybrid_search=True,
            hnsw_kwargs={
                "hnsw_m": 16,
                "hnsw_ef_construction": 64,
                "hnsw_ef_search": 40,
                "hnsw_dist_method": "vector_cosine_ops",
            },
        )

        self.qdrant_vector_store = QdrantVectorStore(
            client=qdrant_client.QdrantClient(
                host="localhost",
                port=6333
            ), 
            collection_name=DIAGNOSIS_STANDARD_TABLE_NAME
        )

        # self.call_build_vector()
        self.pg_vector_index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.pg_vector_store)
        self.qdrant_vector_index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.qdrant_vector_store)

    # def call_build_vector(self):
    #     schedule.every().day.at("02:00").do(self.build_up_document_vector(vector_store_type="qdrant"))
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
    def call_build_vector(self):
        self.build_up_document_vector('qdrant')
        self.build_up_document_vector('pgvector')

        

    def build_up_document_vector(self, vector_store_type: str, db:Session = next(get_db())):
        sql_result = crud.get_diagnosis_standards_for_vector(db)
        if not sql_result:
            raise ValueError("No diagnosis standards found in the database.")
        logger.info(f"Retrieved {len(sql_result)} diagnosis standards for embedding.")
        documents = [Document(text=describes, metadata={"disease_name":name, "type_ab":type_ab, "is_emergency":is_emergency, "urgency_level":urgency_level}, excluded_embed_metadata_keys=['disease_name','type_ab','is_emergency','urgency_level'])  for i, (name, describes,type_ab, is_emergency, urgency_level) in enumerate(sql_result)]
        logger.info(f"Converted to {len(documents)} Document objects for embedding.")
        for doc in documents:
            doc_embedding = self.embed_model.get_text_embedding(doc.get_content(metadata_mode=MetadataMode.EMBED))
            doc.embedding = doc_embedding
        logger.info("Document embeddings generated.")
        if vector_store_type == "pgvector":
            connection = psycopg2.connect(
                dbname=POSTGRES_DATABASE,
                user=POSTGRES_USER_NAME,
                password=POSTGRES_PASSWD,
                host=POSTGRES_HOST,
                port="5432",
                options=f"-c search_path={POSTGRES_SCHEMA}"
            )
            connection.autocommit = True
            table_name = DIAGNOSIS_STANDARD_TABLE_NAME
            with connection.cursor() as c:
                c.execute(f"DROP TABLE IF EXISTS data_{table_name}")
            self.pg_vector_store.add(documents, overwrite=True) 
            self.pg_vecotr_index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.pg_vector_store)
        elif vector_store_type == "qdrant":
            qd_client = qdrant_client.QdrantClient(
                host="localhost",
                port=6333
            )
            qd_client.recreate_collection(  
                collection_name=DIAGNOSIS_STANDARD_TABLE_NAME,
                vectors_config={"size": 1024, "distance": "Cosine"}
            )
            self.qdrant_vector_store.add(documents, overwrite=True)
            self.qdrant_vector_index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.qdrant_vector_store)
        logger.info("Document vectors have been built and stored in the vector store.")



    def embed_search(self, query: str, top_k: int = 5, search_type: str = "hybrid"):
        """
        Perform an embedding-based search on the documents.
        """
        retriever = self.pg_vector_index.as_retriever(similarity_top_k=top_k, vector_store_query_mode=search_type)
        response = retriever.retrieve(query)
        if response is None:
            raise ValueError("Embedding response is None")
        return response

    
    def qdrant_embed_search(self, query: str, top_k: int = 5):
        """
        Perform an embedding-based search on the documents.
        """
        retriever = self.qdrant_vector_index.as_retriever(similarity_top_k=top_k)
        response = retriever.retrieve(query)
        if response is None:
            raise ValueError("Embedding response is None")
        return response


    def reranker_result(self, query: str, documents: str, top_k: int = 3):
        """
        Using external Reranker model to rerank the documents based on the query.
        """
        RERANK_API_URL = RERANK_API_BASE
        HEADERS = {
            "Content-Type": "application/json"
        }
        data = {
            "model": RERANK_MODEL_NAME,
            "query": query,
            "documents": documents,
            "top_n": top_k,
            "truncate_prompt_tokens": 1,
            "additional_data": "string",
            "priority": 0,
            "additionalProp1": {}
        }
        try:
            response = requests.post(
                RERANK_API_URL + "/rerank",
                headers=HEADERS,
                json=data,
                timeout=100
            )
            response.raise_for_status()  # 检查HTTP错误
            results = response.json()['results']
            res = []
            for item in results:
                res.append(item['document']['text'])
            return res
        except requests.exceptions.RequestException as e:
            logger.error(f"Rerank API调用失败: {str(e)}")
            return {"error": str(e)}


if __name__ == "__main__":
    cq = ContentQuery()
