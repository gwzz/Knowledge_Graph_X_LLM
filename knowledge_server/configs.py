import os
from dotenv import load_dotenv
load_dotenv()

LOCAL_SERVER_PORT = 8000

##### model config #####
## Set models
MODEL_NAME = 'qwen3'
LLM_API_BASE = "http://192.168.100.30:8001/v1"

T = 0
MAX_TOKENS = 2048
TIME_OUT = 600

## set embedding model and api
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME')
EMBED_API_BASE       = os.getenv('EMBED_API_BASE')
EMBEDDING_TOP_K      = os.getenv('EMBEDDING_TOP_K')
        

## set rerank model and api
RERANK_MODEL_NAME = os.getenv('RERANK_MODEL_NAME')
RERANK_API_BASE   = os.getenv('RERANK_API_BASE')
RERANK_TOP_K      = os.getenv('RERANK_TOP_K')

FAISS_SCORE = 0.75

##### database config #####
### neo4j config ###
NEO4J_API = os.getenv('NEO4J_API')
NEO4J_USER_NAME = os.getenv('NEO4J_USER_NAME')
NEO4J_PASSWD = os.getenv('NEO4J_PASSWD')

### mysql config ###
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER_NAME = os.getenv('MYSQL_USER_NAME')
MYSQL_PASSWD = os.getenv('MYSQL_PASSWD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

### postgres config ###
POSTGRES_HOST= os.getenv('LOCAL_POSTGRES_HOST')
POSTGRES_USER_NAME = os.getenv('LOCAL_POSTGRES_USER_NAME')
POSTGRES_PASSWD = os.getenv('LOCAL_POSTGRES_PASSWD')
POSTGRES_DATABASE = os.getenv('LOCAL_POSTGRES_DATABASE')
POSTGRES_SCHEMA  = os.getenv('LOCAL_POSTGRES_SCHEMA')

### qdrant config ###
QDRANT_HOST = os.getenv('QDRANT_HOST')

### knowledge table names config ###
DIAGNOSIS_STANDARD_TABLE_NAME = "diagnosis_standards"

### log config ###
LOG_FILE_PATH = "log/log.log"
LOG_LEVEL = "info"
