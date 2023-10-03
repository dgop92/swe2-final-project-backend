import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.logging import config_logger
from config.settings import CORS_ORIGIN_WHITELIST
from routes.people import people_router

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
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGIN_WHITELIST)
app.include_router(people_router, prefix="/people", tags=["people"])


@app.on_event("startup")
def startup():
    logger.info("app started")


@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("app shutdown")
