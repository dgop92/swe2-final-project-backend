from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from core.validations import (
    validate_date,
    validate_document_id,
    validate_document_type,
    validate_operation,
)


class LogItemDetailDTO(BaseModel):
    log_id: str
    operation: str
    document_id: str
    document_type: str
    created_at: datetime


class LogItemCreateDTO(BaseModel):
    operation: str
    document_id: str
    document_type: str
    created_at: datetime

    _validate_operation = field_validator("operation")(validate_operation)
    _validate_document_id = field_validator("document_id")(validate_document_id)
    _validate_document_type = field_validator("document_type")(validate_document_type)
    _validate_created_at = field_validator("created_at")(validate_date)


class LogItemQuery(BaseModel):
    operation: Optional[str] = None
    document_id: Optional[str] = None
    document_type: Optional[str] = None
    created_at_from: Optional[datetime] = None
    created_at_to: Optional[datetime] = None

    _validate_operation = field_validator("operation")(validate_operation)
    _validate_document_id = field_validator("document_id")(validate_document_id)
    _validate_document_type = field_validator("document_type")(validate_document_type)
    _validate_created_at_from = field_validator("created_at_from")(validate_date)
    _validate_created_at_to = field_validator("created_at_to")(validate_date)
