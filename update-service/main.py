import logging

from fastapi import FastAPI

from config.database import get_mongo_database
from config.logging import config_logger
from core.entities import UpdatePeopleDTO
from core.repository import PeopleMongoRepository

config_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="People Update Service",
    description="API to update people for the people service",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)
monog_database = get_mongo_database()
repository = PeopleMongoRepository(monog_database)


@app.patch("/update/{doc_id}")
def update(doc_id: str, data: UpdatePeopleDTO):
    people = repository.update_by_doc_id(doc_id, data)
    return people


@app.on_event("startup")
def startup():
    logger.info("app started")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("app shutdown")
