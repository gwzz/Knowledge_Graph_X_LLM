import re
import json
from configs import *
from json_repair import repair_json
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
from databases import Database
import pandas as pd
import time
import schedule
from threading import Thread




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


class ChatQuery:
    def __init__(self) -> None:
        self.llm = OpenAILike(
            model=MODEL_NAME,
            api_base=LLM_API_BASE,
            # messages_to_prompt=messages_to_prompt,
            # completion_to_prompt=completion_to_prompt,
            api_key='EMPTY',
            is_chat_model=True,
            temperature=T,
            max_tokens=MAX_TOKENS,
            timeout=TIME_OUT,
        ) 

        self.llm_2 = OpenAILike(
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

    def chat_query(self, user_message, **kwargs):
        user_prompt = user_message
        messages = [
            ChatMessage(role="assistant", content="你是一个乐于助人的朋友"),
            ChatMessage(role="user", content=user_prompt)
        ]
        response = self.llm.chat(messages, **kwargs)
        result_str = response.message.content
        print(result_str)
        # if isinstance(response, str):
        #     response = repair_json(response)
        return response
        
    def chat_query_no_think(self, user_message, **kwargs):
        user_prompt = user_message
        messages = [
            ChatMessage(role="assistant", content="你是一个乐于助人的朋友"),
            ChatMessage(role="user", content=user_prompt)
        ]
        response = self.llm_2.chat(messages, **kwargs)
        result_str = response.message.content
        print(result_str)
        # if isinstance(response, str):
        #     response = repair_json(response)
        return response

        



        # self.database = Database()
        # ddff = pd.read_excel('科室数据.xlsx').values.tolist()
        # self.d_nn = {}
        # for i in ddff:
        #     self.d_nn[i[2]] = {"department_top": i[0], "department_id": i[1]}

        # # df = pd.read_excel('faiss_server/dianogsis_with_describes.xlsx')
        # self.start_scheduler()
        # self.data_dict = {}
        # table_data = self.database.query_diagnosis_data()
        # print(table_data)
        # self.table = []
        # for i in table_data:
        #     self.data_dict[i['id']] = {"describe": i.get("describes"), "disease": i.get("name")}
        #     self.table.append(f"{str(i['id'])}、{i.get('describes')}")

    

if __name__ == "__main__":
    gq = GraphQuery()
