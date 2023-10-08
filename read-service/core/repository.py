import logging
from datetime import datetime
from typing import Any, Dict

from pymongo import database

from core.entities import DetailPeopleDTO

logger = logging.getLogger(__name__)


class RepositoryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def from_mongo_to_people_detail(data: Dict[str, Any]) -> DetailPeopleDTO:
    new_date = data["birthDate"].date()
    photo_url = data.get("photoUrl", "https://example.com/photo.jpg")
    new_data = {
        **data,
        "birthDate": new_date,
        "photoUrl": photo_url,
    }
    return DetailPeopleDTO(**new_data)


class PeopleMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing people mongo repository")
        self.collection = db["people"]

    def read_by_doc_id(self, doc_id: str) -> DetailPeopleDTO:
        data = self.collection.find_one({"documentId": doc_id})
        if data is None:
            raise RepositoryException(f"La persona con documento {doc_id} no existe")
        return from_mongo_to_people_detail(data)
