import logging
from json.decoder import JSONDecodeError

from fastapi import Depends, FastAPI, Request
from starlette import status

from config.database import get_mongo_database
from config.logging import config_logger
from core.entities import LogItemQuery
from core.repository import LogItemMongoRepository

config_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Log Service",
    description="API for log operations",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)

mongo_database = get_mongo_database()
repository = LogItemMongoRepository(mongo_database)


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: Request):
    try:
        body = await request.json()
        return body
    except JSONDecodeError:
        return {"message": "Invalid JSON body."}


@app.get("/")
async def list(query: LogItemQuery = Depends()):
    results = repository.list(query)
    return results


@app.get("/{log_id}")
async def detail(log_id: str):
    result = repository.detail(log_id)
    return result


@app.patch("/{log_id}")
async def update(log_id: str):
    return {"log_id": log_id}


@app.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(log_id: str):
    result = repository.delete(log_id)


@app.on_event("startup")
def startup():
    logger.info("log service startup")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("log service shutdown")
