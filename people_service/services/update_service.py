import logging

from fastapi import FastAPI, UploadFile

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


@app.patch("/{doc_id}")
def update(doc_id: str, data: UpdatePeopleDTO):
    people = repository.update_by_doc_id(doc_id, data)
    return people


@app.patch("/{doc_id}/image")
def upload_image(doc_id: str, file: UploadFile):
    people = repository.update_photo_url_doc_id(doc_id, file)
    return people


@app.on_event("startup")
def startup():
    logger.info("update service startup")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("update service shutdown")
