import logging
from json.decoder import JSONDecodeError

from fastapi import FastAPI, Request
from pydantic import ValidationError
from starlette import status

from config.database import get_mongo_database
from config.logging import config_logger
from core.entities import LogItemQuery
from core.repository import LogItemMongoRepository
from core.utils import (
    create_log_item,
    get_detail_uri,
    get_doc_id_and_doc_type,
    get_operation,
)

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
        log_data = await request.json()

        service_name = log_data["service"]["name"]
        operation = get_operation(service_name)
        status_code = log_data["response"]["status"]
        upstream_uri = log_data["upstream_uri"]

        logger.info(
            f"logging info for: {service_name} - URI: {upstream_uri} - OP: {operation} - ST: {status_code}"
        )

        doc_id = None
        doc_type = None
        if service_name == "create-service":
            if status_code == 201:
                doc_id, doc_type = get_doc_id_and_doc_type(
                    log_data["response"].get("body", None)
                )
        elif service_name == "update-service":
            detail_uri = get_detail_uri(upstream_uri)
            if status_code == 200 and detail_uri is not None:
                doc_id, doc_type = get_doc_id_and_doc_type(
                    log_data["response"].get("body", None)
                )
        elif service_name == "read-service":
            detail_uri = get_detail_uri(upstream_uri)
            if status_code == 200 and detail_uri is not None:
                doc_id, doc_type = get_doc_id_and_doc_type(
                    log_data["response"].get("body", None)
                )
        elif service_name == "delete-service":
            detail_uri = get_detail_uri(upstream_uri)
            if status_code == 200 and detail_uri is not None:
                doc_id, doc_type = get_doc_id_and_doc_type(
                    log_data["response"].get("body", None)
                )

        log_item = create_log_item(operation, doc_id, doc_type)
        if doc_id is not None and doc_type is not None:
            logger.info(
                f"creating log item with doc_id: {doc_id} and doc_type: {doc_type}"
            )
            created_log_item = repository.create(log_item)
            return created_log_item
        else:
            logger.info("could not create log item, doc_id and doc_type are None")
            return {"message": "could not create log item"}

    except JSONDecodeError:
        return {"message": "invalid JSON body."}
    except Exception:
        logger.error("could not create log item", exc_info=True)
        return {"message": "could not create log item"}


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
