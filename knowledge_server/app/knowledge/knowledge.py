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
from utils import get_logging
logger = get_logging(__file__)

dotenv.load_dotenv()
# Load embedding and reranker environment variables

                            
# @staticmethod
# def completion_to_prompt(completion):
#     return f"<|im_start|>system\n<|im_end|>\n<|im_start|>user\n{completion}<|im_end|>\n<|im_start|>assistant\n"

# @staticmethod
# def messages_to_prompt(messages):
#     prompt = ""
#     for message in messages:
#         if message.role == "system":
#             prompt += f"<|im_start|>system\n{message.content}<|im_end|>\n"
#         elif message.role == "user":
#             prompt += f"<|im_start|>user\n{message.content}<|im_end|>\n"
#         elif message.role == "assistant":
#             prompt += f"<|im_start|>assistant\n{message.content}<|im_end|>\n"

#     if not prompt.startswith("<|im_start|>system"):
#         prompt = "<|im_start|>system\n" + prompt

#     prompt = prompt + "<|im_start|>assistant\n"

#     return prompt


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

        self.vector_store = PGVectorStore.from_params(
            database='hospital_standards',
            host=POSTGRES_HOST,
            password=POSTGRES_PASSWD,
            port=5432,
            user=POSTGRES_USER_NAME,
            table_name="diagnosis_standards",
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
            collection_name="diagnosis_standards")

        ##### below are test methods for dev #####
        # self.build_up_document_vector_pgvector()
        # self.build_up_document_vector_qdrant()
        # self.embed_search("甲状腺", top_k=5)  # Test embedding search
        # self.qdrant_embed_search("甲状腺", top_k=5)

    def build_up_document_vector_pgvector(self, db:Session = next(get_db())):
        sql_result = crud.get_diagnosis_standards_for_vector(db)
        if not sql_result:
            raise ValueError("No diagnosis standards found in the database.")
        logger.info(f"Retrieved {len(sql_result)} diagnosis standards for embedding.")
        documents = [Document(text=describes, metadata={"disease_name":name}, excluded_embed_metadata_keys=['disease_name'])  for i, (name, describes) in enumerate(sql_result)]
        for doc in documents:
            doc_embedding = self.embed_model.get_text_embedding(doc.get_content(metadata_mode=MetadataMode.EMBED))
            doc.embedding = doc_embedding
        self.vector_store.add(documents, overwrite=True) 
        logger.info("Document vectors have been built and stored in the vector store.")


    def build_up_document_vector_qdrant(self, db:Session = next(get_db())):
        sql_result = crud.get_diagnosis_standards_for_vector(db)
        if not sql_result:
            raise ValueError("No diagnosis standards found in the database.")
        logger.info(f"Retrieved {len(sql_result)} diagnosis standards for embedding.")
        
        documents = [Document(text=describes, metadata={"disease_name":name}, excluded_embed_metadata_keys=['disease_name'])  for i, (name, describes) in enumerate(sql_result)]
        for doc in documents:
            doc_embedding = self.embed_model.get_text_embedding(doc.get_content(metadata_mode=MetadataMode.EMBED))
            doc.embedding = doc_embedding
        self.qdrant_vector_store.add(documents, overwrite=True)
        logger.info("Document vectors have been built and stored in the Qdrant vector store.")

        # client = qdrant_client.QdrantClient(host="localhost", port=6333)
        # vector_store = QdrantVectorStore(client=client, collection_name="diagnosis_standards")
        # storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # index = VectorStoreIndex.from_documents(
        #     embed_model=self.embed_model,
        #     documents=documents,
        #     storage_context=storage_context,
        # )


    def embed_search(self, query: str, top_k: int = 5, search_type: str = "hybrid"):
        """
        Perform an embedding-based search on the documents.
        """
        vector_index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.vector_store)
        retriever = vector_index.as_retriever(similarity_top_k=top_k, vector_store_query_mode=search_type)
        response = retriever.retrieve(query)
        print(response)
        if response is None:
            raise ValueError("Embedding response is None")
        return response
    
    def qdrant_embed_search(self, query: str, top_k: int = 5):
        """
        Perform an embedding-based search on the documents.
        """
        vector_index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.qdrant_vector_store)
        retriever = vector_index.as_retriever(similarity_top_k=top_k)
        response = retriever.retrieve(query)
        print(response)
        if response is None:
            raise ValueError("Embedding response is None")
        return response


    def reranker_result(self, query: str, documents: str, top_k: int = 3):
        """
        Rerank the results based on the query.
        """
        response = self.llm.rerank(query, documents, top_k=top_k)
        if response is None:
            raise ValueError("Reranker response is None")
        return response

if __name__ == "__main__":
    gq = ContentQuery()
