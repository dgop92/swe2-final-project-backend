import logging

from fastapi import FastAPI
from starlette import status

from config.database import get_mongo_database
from config.logging import config_logger
from core.repository import PeopleMongoRepository

config_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="People Delete Service",
    description="API to delete people for the people service",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)
monog_database = get_mongo_database()
repository = PeopleMongoRepository(monog_database)


@app.delete("/{doc_id}", status_code=status.HTTP_200_OK)
def delete(doc_id: str):
    people = repository.delete_by_doc_id(doc_id)
    return people


@app.on_event("startup")
def startup():
    logger.info("delete service startup")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("delete service shutdown")
