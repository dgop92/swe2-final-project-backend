import logging
from datetime import datetime

from pymongo import database

from core.entities import CreatePeopleDTO

logger = logging.getLogger(__name__)


class RepositoryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PeopleMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing people mongo repository")
        self.collection = db["people"]

    def create(self, people: CreatePeopleDTO) -> CreatePeopleDTO:
        logger.info(f"creating people with documentId {people.documentId}")
        # check if a document with the same documentId already exists
        if self.collection.find_one({"documentId": people.documentId}):
            raise RepositoryException(
                f"Una persona con el documento {people.documentId} ya existe"
            )
        people_as_dict = people.model_dump()
        people_birth_date = people_as_dict["birthDate"]
        # to datetime
        people_as_dict["birthDate"] = datetime.combine(
            people_birth_date, datetime.min.time()
        )
        self.collection.insert_one(people_as_dict)
        return people