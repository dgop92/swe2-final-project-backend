from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from core.validations import (
    validate_birth_date,
    validate_document_id,
    validate_document_type,
    validate_email,
    validate_first_name,
    validate_gender,
    validate_last_name,
    validate_middle_name,
    validate_phone,
)


class DetailPeopleDTO(BaseModel):
    document_type: str
    document_id: str
    first_name: str
    middle_name: str
    last_name: str
    birth_date: date
    gender: str
    email: str
    phone: str
    photo_url: str = "https://example.com/photo.jpg"


class CreatePeopleDTO(BaseModel):
    document_type: str
    document_id: str
    first_name: str
    middle_name: str
    last_name: str
    birth_date: date
    gender: str
    email: str
    phone: str

    _validate_document_type = field_validator("document_type")(validate_document_type)
    _validate_document_id = field_validator("document_id")(validate_document_id)
    _validate_first_name = field_validator("first_name")(validate_first_name)
    _validate_middle_name = field_validator("middle_name")(validate_middle_name)
    _validate_last_name = field_validator("last_name")(validate_last_name)
    _validate_birth_date = field_validator("birth_date", mode="before")(
        validate_birth_date
    )
    _validate_gender = field_validator("gender")(validate_gender)
    _validate_email = field_validator("email")(validate_email)
    _validate_phone = field_validator("phone")(validate_phone)


class UpdatePeopleDTO(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    _validate_first_name = field_validator("first_name")(validate_first_name)
    _validate_middle_name = field_validator("middle_name")(validate_middle_name)
    _validate_last_name = field_validator("last_name")(validate_last_name)
    _validate_birth_date = field_validator("birth_date", mode="before")(
        validate_birth_date
    )
    _validate_gender = field_validator("gender")(validate_gender)
    _validate_email = field_validator("email")(validate_email)
    _validate_phone = field_validator("phone")(validate_phone)
