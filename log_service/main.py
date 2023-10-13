import logging
from json.decoder import JSONDecodeError

from fastapi import FastAPI, Request
from pydantic import ValidationError
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
def list(
    operation: str = None,
    document_id: str = None,
    document_type: str = None,
    created_at_from: str = None,
    created_at_to: str = None,
):
    try:
        query = LogItemQuery(
            operation=operation,
            document_id=document_id,
            document_type=document_type,
            created_at_from=created_at_from,
            created_at_to=created_at_to,
        )
        results = repository.list(query)
        return results
    except ValidationError as e:
        return {"detail": e.errors()}


@app.get("/{log_id}")
def detail(log_id: str):
    result = repository.detail(log_id)
    return result


@app.patch("/{log_id}")
def update(log_id: str):
    return {"log_id": log_id}


@app.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(log_id: str):
    repository.delete(log_id)


@app.on_event("startup")
def startup():
    logger.info("log service startup")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("log service shutdown")
