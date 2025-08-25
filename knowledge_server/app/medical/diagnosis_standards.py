import re
import json
import os
import dotenv
from configs import *
from llama_index.llms.openai_like import OpenAILike
from utils import get_logging
logger = get_logging(__file__)

dotenv.load_dotenv()


class MedicalQuery:
    def __init__(self) -> None:
        self.llm = OpenAILike(
            model=MODEL_NAME,
            api_base=LLM_API_BASE,
            api_key='EMPTY',
            is_chat_model=True,
            temperature=0.6,
            max_tokens=MAX_TOKENS,
            timeout=TIME_OUT,
            additional_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        )

    def search_diagnosis_rag(self, query:str, embed_results:list, rerank_results:list):
        """
        Using embedding and reranker model to search the diagnosis standards based on the query.
        """
        print(f"query: {query}")
        response = [item for item in embed_results if item.text in rerank_results]
        logger.info(f"RAG结果: {response}")
        if response is None:
            raise ValueError("Medical RAG search_diagnosis is None")
        return response




if __name__ == "__main__":
    mq = MedicalQuery()
