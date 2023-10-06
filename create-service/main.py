import logging

from fastapi import FastAPI

from config.logging import config_logger
from core.entities import People

config_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="People API",
    description="API to manage people",
    contact={
        "name": "dgop92",
        "url": "https://github.com/dgop92",
    },
)


@app.post("/create")
def create(people: People):
    return people


@app.on_event("startup")
def startup():
    logger.info("app started")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("app shutdown")
