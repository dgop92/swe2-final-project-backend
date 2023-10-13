from datetime import datetime
from typing import Any


def validate_document_id(v: str | None) -> str | None:
    if v is None:
        return v

    if not v.isnumeric():
        raise ValueError("El número de documento debe ser un número")
    if len(v) > 10:
        raise ValueError("El número de documento no puede tener más de 10 caracteres")
    return v


def validate_document_type(v: str | None) -> str | None:
    if v is None:
        return v

    valid_document_types = ["Tarjeta de identidad", "Cédula"]
    if v not in valid_document_types:
        raise ValueError(
            f'El tipo de documento debe ser uno de los siguientes: {", ".join(valid_document_types)}'
        )
    return v


def validate_operation(v: str | None) -> str | None:
    if v is None:
        return v

    valid_operations = ["create", "update", "delete", "read"]
    if v not in valid_operations:
        raise ValueError(
            f'La operación debe ser una de las siguientes: {", ".join(valid_operations)}'
        )

    return v


def validate_date(v: Any) -> Any:
    if v is None:
        return v

    if isinstance(v, datetime):
        return v

    try:
        date_object = datetime.strptime(v, "%d-%m-%Y")
    except Exception:
        raise ValueError("La fecha debe estar escrita en formato dd-mm-yyyy")
    return date_object
