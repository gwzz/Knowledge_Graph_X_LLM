import re
import json
from configs import *
from json_repair import repair_json
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai_like import OpenAILike
import mlflow
from mlflow.genai.scorers import Correctness, Guidelines
from mlflow.genai import scorer


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
            api_key='EMPTY',
            is_chat_model=True,
            temperature=T,
            max_tokens=MAX_TOKENS,
            timeout=TIME_OUT,
        ) 

        self.llm_2 = OpenAILike(
            model=MODEL_NAME,
            api_base=LLM_API_BASE,
            api_key='EMPTY',
            is_chat_model=True,
            temperature=0.6,
            max_tokens=MAX_TOKENS,
            timeout=TIME_OUT,
            additional_kwargs={"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}},
        )
        mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # @mlflow.trace
    def chat_query(self, user_message, **kwargs):
        mlflow.set_experiment(experiment_id="0")
        mlflow.llama_index.autolog()
        user_prompt = user_message
        messages = [
            ChatMessage(role="assistant", content="你是一个乐于助人的朋友"),
            ChatMessage(role="user", content=user_prompt)
        ]
        response = self.llm.chat(messages, **kwargs)
        # result_str = response.message.content
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

### below is for mlflow test
    def predict_fn(self, question: str, **kwargs) -> str:
        user_prompt = question
        print(f"user_prompt: {user_prompt}")
        messages = [
            ChatMessage(role="assistant", content="你是一个乐于回答问题的全科医生。你只回答“是” 或 “否”。"),
            ChatMessage(role="user", content=user_prompt)
        ]
        response = self.llm_2.chat(messages, **kwargs)
        print(f"response: {response.message.blocks[0].text}")
        return response.message.blocks[0].text

    @scorer
    def exact_match(outputs: dict, expectations: dict) -> bool:
        return outputs == expectations["expected_response"]

    def mlflow_test(self, **kwargs):
        dataset = [
            {
                "inputs": {"question": "我的空腹血糖10mmol，是有糖尿病风险吗？"},
                "expectations": {"expected_response": "是。"},
            },
            {
                "inputs": {"question": "我头疼，是不是马上要死了？"},
                "expectations": {
                    "expected_response": "否。"
                },
            },
            {
                "inputs": {"question": "我的血压值为150/110，我有高血压风险吗？"},
                "expectations": {
                    "expected_response": "是。"
                },
            },
            {
                "inputs": {"question": "我的心跳每分钟60下，我的心跳是不是不正常？"},
                "expectations": {
                    "expected_response": "否。"
                },
            },
        ]
        results = mlflow.genai.evaluate(
            data=dataset,
            predict_fn=self.predict_fn,
            scorers=[self.exact_match
            ],
        )
        print(results)

if __name__ == "__main__":
    cq = ChatQuery()
