from datetime import datetime
from typing import Any


def validate_document_id(v: str) -> str:
    if not v.isnumeric():
        raise ValueError("El número de documento debe ser un número")
    if len(v) > 10:
        raise ValueError("El número de documento no puede tener más de 10 caracteres")
    return v


def validate_document_type(v: str) -> str:
    valid_document_types = ["Tarjeta de identidad", "Cédula"]
    if v not in valid_document_types:
        raise ValueError(
            f'El tipo de documento debe ser uno de los siguientes: {", ".join(valid_document_types)}'
        )
    return v


def validate_first_name(v: str) -> str:
    if v.isnumeric():
        raise ValueError("El primer nombre no puede ser un número")
    if len(v) > 30:
        raise ValueError("El primer nombre no puede tener más de 30 caracteres")
    return v


def validate_middle_name(v: str) -> str:
    if v.isnumeric():
        raise ValueError("El segundo nombre no puede ser un número")
    if len(v) > 30:
        raise ValueError("El segundo nombre no puede tener más de 30 caracteres")
    return v


def validate_last_name(v: str) -> str:
    if v.isnumeric():
        raise ValueError("El apellido no puede ser un número")
    if len(v) > 60:
        raise ValueError("El apellido no puede tener más de 60 caracteres")
    return v


def validate_gender(v: str) -> str:
    valid_genders = ["Masculino", "Femenino", "No binario", "Prefiero no decir"]
    if v not in valid_genders:
        raise ValueError(
            f'El género debe ser uno de los siguientes: {", ".join(valid_genders)}'
        )
    return v


def validate_birth_date(v: Any) -> Any:
    if v is None:
        return v

    try:
        date_object = datetime.strptime(v, "%d-%m-%Y").date()
    except Exception:
        raise ValueError(
            "La fecha de nacimiento debe estar escrita en formato dd-mm-yyyy"
        )
    return date_object


def validate_email(v: str) -> str:
    import re

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, v):
        raise ValueError("Formato de correo electrónico inválido")
    return v


def validate_phone(v: str) -> str:
    if not v.isnumeric():
        raise ValueError("El número de teléfono debe ser un número")
    if len(v) != 10:
        raise ValueError("El número de teléfono debe tener 10 caracteres")
    return v
