import re
import json
import os
import dotenv
from configs import *
from json_repair import repair_json
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Document,VectorStoreIndex,Settings

from llama_index.vector_stores.postgres import PGVectorStore

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
        )
        self.query_diagnosis_standard()
        self.embed_search("甲状腺结节", top_k=5)  # Test embedding search
        
    def query_diagnosis_standard(self, db:Session = next(get_db())):
        sql_result = crud.get_diagnosis_standards_for_vector(db)
        if not sql_result:
            raise ValueError("No diagnosis standards found in the database.")
        
        print('Embedding completed, starting to insert into vector store...')
            
        documents = [Document(text=describes, metadata={"disease_name":name})  for i, (name, describes) in enumerate(sql_result)]
        for doc in documents:
            doc_embedding = self.embed_model.get_text_embedding(doc.get_content(metadata_mode="all"))
            doc.embedding = doc_embedding
        self.vector_store.add(documents, overwrite=True) 
        print('Inserted into vector store successfully.')
        #     doc.embedding = doc_embedding
        
 
        
    def build_document_vector(self, content: str):
        """
        Build document vector using the embedding model.
        """
        response = self.llm.embed(content)
        if response is None:
            raise ValueError("Embedding response is None")
        return response
    

    def embed_search(self, query: str, top_k: int = 3):
        """
        Perform an embedding-based search on the documents.
        """
        index = VectorStoreIndex.from_vector_store(embed_model=self.embed_model,vector_store = self.vector_store)
        # print(index)
        # index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store, emded_model=Settings.default_embedding_model)
        retriever = index.as_retriever(similarity_top_k=5)
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
