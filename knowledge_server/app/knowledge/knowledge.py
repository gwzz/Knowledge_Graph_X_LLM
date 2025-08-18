import re
import json
import os
import dotenv
from configs import *
from json_repair import repair_json
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
import pandas as pd
import time
import schedule
from threading import Thread


dotenv.load_dotenv()
# Load embedding and reranker environment variables
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")
EMBED_API_BASE = os.getenv("EMBED_API_BASE")
EMBEDDING_TOP_K = os.getenv("EMBEDDING_TOP_K")

RERANK_MODEL_NAME = os.getenv("RERANK_MODEL_NAME")
RERANK_API_BASE = os.getenv("RERANK_API_BASE")
RERANK_TOP_K = os.getenv("RERANK_TOP_K")

                            
@staticmethod
def completion_to_prompt(completion):
    return f"<|im_start|>system\n<|im_end|>\n<|im_start|>user\n{completion}<|im_end|>\n<|im_start|>assistant\n"

@staticmethod
def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == "system":
            prompt += f"<|im_start|>system\n{message.content}<|im_end|>\n"
        elif message.role == "user":
            prompt += f"<|im_start|>user\n{message.content}<|im_end|>\n"
        elif message.role == "assistant":
            prompt += f"<|im_start|>assistant\n{message.content}<|im_end|>\n"

    if not prompt.startswith("<|im_start|>system"):
        prompt = "<|im_start|>system\n" + prompt

    prompt = prompt + "<|im_start|>assistant\n"

    return prompt


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
        
    
    def build_document_vector(self, content: str):
        """
        Build document vector using the embedding model.
        """
        response = self.llm.embed(content)
        if response is None:
            raise ValueError("Embedding response is None")
        return response
    

    def embed_search(self, query: str, documents: str, top_k: int = 3):
        """
        Perform an embedding-based search on the documents.
        """
        response = ""
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
