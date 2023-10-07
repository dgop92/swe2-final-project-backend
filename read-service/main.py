import logging

from fastapi import FastAPI, HTTPException

from config.database import get_mongo_database
from config.logging import config_logger

# from core.entities import CreatePeopleDTO
from core.repository import PeopleMongoRepository, RepositoryException

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


@app.get("/detail/{doc_id}")
def detail(doc_id: str):
    try:
        people = repository.read_by_doc_id(doc_id)
        return people
    except RepositoryException as e:
        logger.error(e)
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@app.on_event("startup")
def startup():
    logger.info("app started")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("app shutdown")
