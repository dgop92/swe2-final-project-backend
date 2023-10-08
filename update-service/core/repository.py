import logging
from datetime import datetime
from typing import Any, Dict

import cloudinary.api
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
from pymongo import database

from core.entities import DetailPeopleDTO, UpdatePeopleDTO

logger = logging.getLogger(__name__)


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
            raise HTTPException(
                status_code=404, detail=f"La persona con documento {doc_id} no existe"
            )
        return from_mongo_to_people_detail(data)

    def update_by_doc_id(self, doc_id: str, data: UpdatePeopleDTO) -> DetailPeopleDTO:
        logger.info(f"retrieving people with documentId {doc_id}")
        people = self.read_by_doc_id(doc_id)
        to_update_data = data.model_dump()
        # remove None values
        to_update_data = {k: v for k, v in to_update_data.items() if v is not None}
        update_data_keys = to_update_data.keys()
        logger.info(f"updating people properties {update_data_keys}")

        if "birthDate" in update_data_keys:
            to_update_data["birthDate"] = to_update_data[
                "birthDate"
            ] = datetime.combine(to_update_data["birthDate"], datetime.min.time())

        if len(to_update_data) == 0:
            return people

        self.collection.update_one({"documentId": doc_id}, {"$set": to_update_data})

        old_people_data = people.model_dump()
        new_people_data = {**old_people_data, **to_update_data}

        return DetailPeopleDTO(**new_people_data)

    def update_photo_url_doc_id(
        self, doc_id: str, uploaded_file: UploadFile
    ) -> DetailPeopleDTO:
        logger.info(f"retrieving people with documentId {doc_id}")
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
        new_people.photoUrl = photo_url

        logger.info(f"updating people photoUrl")
        self.collection.update_one(
            {"documentId": doc_id}, {"$set": {"photoUrl": photo_url}}
        )

        return new_people
