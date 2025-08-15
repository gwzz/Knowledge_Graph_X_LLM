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
EMBEDDING_MODEL_NAME = "bge-embedding"
EMBED_API_BASE = "http://192.168.100.30:12001/v1"

## set rerank model and api
RERANK_MODEL_NAME = "bge-reranker"
RERANK_API_BASE = "http://192.168.100.30:12002/v1"

FAISS_SCORE = 0.75
TOP_K = 1

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

### log config ###
LOG_FILE_PATH = "log/log.log"
LOG_LEVEL = "info"
