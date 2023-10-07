import logging

from pymongo import database

logger = logging.getLogger(__name__)


class RepositoryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PeopleMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing people mongo repository")
        self.collection = db["people"]

    def delete_by_doc_id(self, doc_id: str) -> None:
        data = self.collection.find_one({"documentId": doc_id})
        if data is None:
            raise RepositoryException(f"La persona con documento {doc_id} no existe")
        self.collection.delete_one({"documentId": doc_id})
