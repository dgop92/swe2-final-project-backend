import logging
from typing import Any, Dict, List

from fastapi import HTTPException
from pymongo import database

from core.entities import LogItemCreateDTO, LogItemDetailDTO, LogItemQuery

logger = logging.getLogger(__name__)


def from_mongo_data_to_log_item(data: Dict[str, Any]) -> LogItemDetailDTO:
    return LogItemDetailDTO(
        log_id=str(data["_id"]),
        operation=data["operation"],
        document_id=data["document_id"],
        document_type=data["document_type"],
        created_at=data["created_at"],
    )


class LogItemMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing log_item mongo repository")
        self.collection = db["logs"]

    def create(self, log_item: LogItemCreateDTO) -> LogItemDetailDTO:
        log_item_as_dict = log_item.model_dump()
        result = self.collection.insert_one(log_item_as_dict)
        log_id = str(result.inserted_id)
        log_item_data = {
            **log_item_as_dict,
            "log_id": log_id,
        }
        return LogItemDetailDTO(**log_item_data)

    def list(self, query: LogItemQuery) -> List[LogItemDetailDTO]:
        query_as_dict = query.model_dump()

        mongo_query = {}

        if "operation" in query_as_dict:
            mongo_query["operation"] = query_as_dict["operation"]

        if "document_id" in query_as_dict:
            mongo_query["document_id"] = query_as_dict["document_id"]

        if "document_type" in query_as_dict:
            mongo_query["document_type"] = query_as_dict["document_type"]

        if "created_at_from" in query_as_dict:
            mongo_query["created_at"] = {
                **mongo_query.get("created_at", {}),
                "$gte": query_as_dict["created_at_from"],
            }

        if "created_at_to" in query_as_dict:
            mongo_query["created_at"] = {
                **mongo_query.get("created_at", {}),
                "$lte": query_as_dict["created_at_to"],
            }

        result = self.collection.find(mongo_query)

        return [from_mongo_data_to_log_item(data) for data in result]

    def detail(self, log_id: str) -> LogItemDetailDTO:
        result = self.collection.find_one({"_id": log_id})
        if not result:
            raise HTTPException(status_code=404, detail="el registro no existe")
        return from_mongo_data_to_log_item(result)

    def delete(self, log_id: str):
        result = self.collection.delete_one({"_id": log_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="el registro no existe")
        return None
