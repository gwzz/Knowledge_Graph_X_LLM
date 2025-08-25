import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from app.chat.chat import ChatQuery
from configs import *
from utils import get_logging
from sqlalchemy.orm import Session
from app.knowledge import knowledge_crud as crud
from app.knowledge import knowledge_schemas as schemas
from app.knowledge import knowledge_models as models
from databases import engine, get_db
from app.knowledge.knowledge import ContentQuery
from app.medical.diagnosis_standards import MedicalQuery
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)  # 创建数据库表

# 创建FastAPI应用
app = FastAPI()
chat = ChatQuery()
logger = get_logging(__file__)
content = ContentQuery()
medicalrag = MedicalQuery()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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


## database crud operations
@app.post("/knowledge/diagnosis_standards/", response_model=schemas.DiagnosisStandard)
async def create_diagnosis_standard(diagnosis: schemas.DiagnosisStandardCreate, db: Session = Depends(get_db)):
    return crud.create_diagnosis_standard(db, diagnosis)

@app.get("/knowledge/diagnosis_standards/", response_model=list[schemas.DiagnosisStandard])
async def read_diagnosis_standards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_diagnosis_standards(db, skip, limit)

@app.get("/knowledge/diagnosis_standards/{diagnosis_id}", response_model=schemas.DiagnosisStandard)
async def read_diagnosis_standard(diagnosis_id: int, db: Session = Depends(get_db)):
    db_diagnosis = crud.get_diagnosis_standard(db, diagnosis_id)
    if not db_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis standard not found")
    return db_diagnosis

@app.put("/knowledge/diagnosis_standards/{diagnosis_id}", response_model=schemas.DiagnosisStandard)
async def update_diagnosis_standard(diagnosis_id: int, diagnosis: schemas.DiagnosisStandardBase, db: Session = Depends(get_db)):
    db_diagnosis = crud.update_diagnosis_standard(db, diagnosis_id, diagnosis)
    if not db_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis standard not found")
    return db_diagnosis

@app.delete("/knowledge/diagnosis_standards/{diagnosis_id}", response_model=schemas.DiagnosisStandard)
async def delete_diagnosis_standard(diagnosis_id: int, db: Session = Depends(get_db)):
    db_diagnosis = crud.delete_diagnosis_standard(db, diagnosis_id)
    if not db_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis standard not found")
    return db_diagnosis

@app.put("/knowledge/build_vector")
async def build_vector_endpoint():
    try:
        content.call_build_vector()
        return {"status": "Vector built successfully"}
    except Exception as e:
        logger.error(f"Error initiating vector building: {e}")
        raise HTTPException(status_code=500, detail="Error initiating vector building")

@app.post("/knowledge/embed_search")
async def embed_search_endpoint(request: Request):
    data = await request.json()
    logger.info(f"入参: {data}")
    query = data.get("query", "")
    top_k = data.get("top_k", 5)
    if not query:
        return {"error": "No query provided"}
    
    response = content.embed_search(query, top_k=top_k)
    return {"response": response}

@app.post("/knowledge/qdrant_embed_search")
async def embed_search_endpoint(request: Request):
    data = await request.json()
    logger.info(f"入参: {data}")
    query = data.get("query", "")
    top_k = data.get("top_k", 5)
    if not query:
        return {"error": "No query provided"}
    
    response = content.qdrant_embed_search(query, top_k=top_k)
    return {"response": response}

@app.post("/knowledge/reranker_search")
async def reranker_search_endpoint(request: Request):
    data = await request.json()
    logger.info(f"入参: {data}")
    query = data.get("query", "")
    documents = data.get("documents", "")
    top_k = data.get("top_k", 3)
    if not query or not documents:
        return {"error": "No query or documents provided"}
    
    response = content.reranker_result(query, documents, top_k=top_k)
    return {"response": response}

class medical_rag_request_json(BaseModel):
    query:str
    embed_top_k:int
    rerank_top_k:int
@app.post("/medical/diagnosis_standards_rag")
async def diagnosis_standards_rag_endpoint(request: medical_rag_request_json):
    logger.info(f"入参: {request}")
    query = request.query
    embed_top_k = request.embed_top_k
    rerank_top_k = request.rerank_top_k
    if not query:
        return {"error": "No query provided"}
    embed_results = content.qdrant_embed_search(query, top_k=embed_top_k)
    rerank_results = content.reranker_result(query, [item.text for item in embed_results], top_k=rerank_top_k)
    response = medicalrag.search_diagnosis_rag(query, embed_results, rerank_results)

    return {"response": response}

if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=8001, workers=1)  # 在指定端口和主机上启动应用