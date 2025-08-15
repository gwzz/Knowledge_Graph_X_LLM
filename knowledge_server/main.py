import uvicorn
from fastapi import FastAPI, Request
from app.chat import ChatQuery
from configs import *
from utils import get_logging

# 创建FastAPI应用
app = FastAPI()
chat = ChatQuery()
logger = get_logging(__file__)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    logger.info(f"入参: {data}")
    user_message = data.get("message", "")
    if not user_message:
        return {"error": "No message provided"}
    
    response = chat.chat_query(user_message)
    return {"response": response}

@app.post("/chat_no_think")
async def chat_no_think_endpoint(request: Request):
    data = await request.json()
    logger.info(f"入参: {data}")
    user_message = data.get("message", "")
    if not user_message:
        return {"error": "No message provided"}
    
    response = chat.chat_query_no_think(user_message)
    return {"response": response}




# 主函数入口
if __name__ == '__main__':
    # 启动FastAPI应用，用6006端口映射到本地，从而在本地使用api
    uvicorn.run(app, host='0.0.0.0', port=8001, workers=1)  # 在指定端口和主机上启动应用