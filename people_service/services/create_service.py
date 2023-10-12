import logging

from fastapi import FastAPI
from starlette import status

from config.database import get_mongo_database
from config.logging import config_logger
from core.entities import CreatePeopleDTO
from core.repository import PeopleMongoRepository

config_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="People Create Service",
    description="API to create people for the people service",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)
mongo_database = get_mongo_database()
repository = PeopleMongoRepository(mongo_database)


@app.post("/", status_code=status.HTTP_201_CREATED)
def create(people: CreatePeopleDTO):
    created_people = repository.create(people)
    return created_people


@app.on_event("startup")
def startup():
    logger.info("create service startup")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("create service shutdown")
