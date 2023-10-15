import logging
from datetime import datetime
from typing import Any, Dict, List

import cloudinary.api
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
from pymongo import database

from core.entities import CreatePeopleDTO, DetailPeopleDTO, UpdatePeopleDTO

logger = logging.getLogger(__name__)


def from_mongo_to_people_detail(data: Dict[str, Any]) -> DetailPeopleDTO:
    new_date = data["birth_date"].date()
    photo_url = data.get("photo_url", "https://example.com/photo.jpg")
    new_data = {
        **data,
        "birth_date": new_date,
        "photo_url": photo_url,
    }
    return DetailPeopleDTO(**new_data)


class PeopleMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing people mongo repository")
        self.collection = db["people"]

    def create(self, people: CreatePeopleDTO) -> DetailPeopleDTO:
        logger.info(f"creating people with document_id {people.document_id}")
        # check if a document with the same document_id already exists
        if self.collection.find_one({"document_id": people.document_id}):
            raise HTTPException(
                status_code=404,
                detail=f"Una persona con el documento {people.document_id} ya existe",
            )
        people_as_dict = people.model_dump()
        people_birth_date = people_as_dict["birth_date"]
        # to datetime
        people_as_dict["birth_date"] = datetime.combine(
            people_birth_date, datetime.min.time()
        )
        self.collection.insert_one(people_as_dict)
        return from_mongo_to_people_detail(people_as_dict)

    def read_by_doc_id(self, doc_id: str) -> DetailPeopleDTO:
        data = self.collection.find_one({"document_id": doc_id})
        if data is None:
            raise HTTPException(
                status_code=404, detail=f"La persona con documento {doc_id} no existe"
            )
        return from_mongo_to_people_detail(data)

    def list(self) -> List[DetailPeopleDTO]:
        data = self.collection.find({})
        return [from_mongo_to_people_detail(d) for d in data]

    def update_by_doc_id(self, doc_id: str, data: UpdatePeopleDTO) -> DetailPeopleDTO:
        logger.info(f"retrieving people with document_id {doc_id}")
        people = self.read_by_doc_id(doc_id)
        to_update_data = data.model_dump()
        # remove None values
        to_update_data = {k: v for k, v in to_update_data.items() if v is not None}
        update_data_keys = to_update_data.keys()
        logger.info(f"updating people properties {update_data_keys}")

        if "birth_date" in update_data_keys:
            to_update_data["birth_date"] = to_update_data[
                "birth_date"
            ] = datetime.combine(to_update_data["birth_date"], datetime.min.time())

        if len(to_update_data) == 0:
            return people

        self.collection.update_one({"document_id": doc_id}, {"$set": to_update_data})

        old_people_data = people.model_dump()
        new_people_data = {**old_people_data, **to_update_data}

        return DetailPeopleDTO(**new_people_data)

    def update_photo_url_doc_id(
        self, doc_id: str, uploaded_file: UploadFile
    ) -> DetailPeopleDTO:
        logger.info(f"retrieving people with document_id {doc_id}")
        people = self.read_by_doc_id(doc_id)

        # file cannot be larger than 2MB
        if uploaded_file.size > 2 * 1024 * 1024:
            raise HTTPException(
                status_code=400, detail="La imagen no puede ser mayor a 2MB"
            )

        # file must a png or jpg
        if uploaded_file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            raise HTTPException(
                status_code=400, detail="La imagen debe ser png, jpg o jpeg"
            )

        logger.info(f"uploading image to cloudinary")
        upload_result = cloudinary.uploader.upload(
            uploaded_file.file, folder="people_service"
        )

        photo_url = upload_result["secure_url"]
        new_people = people.model_copy()
        new_people.photo_url = photo_url

        logger.info(f"updating people photo_url")
        self.collection.update_one(
            {"document_id": doc_id}, {"$set": {"photo_url": photo_url}}
        )

        return new_people

    def delete_by_doc_id(self, doc_id: str) -> DetailPeopleDTO:
        people = self.read_by_doc_id(doc_id)
        logger.info(f"deleting people with document_id {doc_id}")
        self.collection.delete_one({"document_id": doc_id})
        logger.info(f"people with document_id {doc_id} deleted")
        return people
