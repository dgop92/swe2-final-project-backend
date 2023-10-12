import logging

from fastapi import FastAPI

from config.database import get_mongo_database
from config.logging import config_logger
from core.repository import PeopleMongoRepository

config_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="People Search Service",
    description="API to search people for the people service",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)
monog_database = get_mongo_database()
repository = PeopleMongoRepository(monog_database)


@app.get("/")
def list():
    people_list = repository.list()
    return people_list


@app.get("/{doc_id}")
def detail(doc_id: str):
    people = repository.read_by_doc_id(doc_id)
    return people


@app.on_event("startup")
def startup():
    logger.info("read service startup")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("read service shutdown")
