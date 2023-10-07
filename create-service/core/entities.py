from datetime import date, datetime

from pydantic import BaseModel, field_validator


class CreatePeopleDTO(BaseModel):
    documentType: str
    documentId: str
    firstName: str
    middleName: str
    lastName: str
    birthDate: date
    gender: str
    email: str
    phone: str

    @field_validator("firstName")
    @classmethod
    def validate_first_name(cls, v):
        if v.isnumeric():
            raise ValueError("El primer nombre no puede ser un número")
        if len(v) > 30:
            raise ValueError("El primer nombre no puede tener más de 30 caracteres")
        return v

    @field_validator("middleName")
    @classmethod
    def validate_middle_name(cls, v):
        if v.isnumeric():
            raise ValueError("El segundo nombre no puede ser un número")
        if len(v) > 30:
            raise ValueError("El segundo nombre no puede tener más de 30 caracteres")
        return v

    @field_validator("lastName")
    @classmethod
    def validate_last_name(cls, v):
        if v.isnumeric():
            raise ValueError("El apellido no puede ser un número")
        if len(v) > 60:
            raise ValueError("El apellido no puede tener más de 60 caracteres")
        return v

    @field_validator("birthDate", mode="before")
    @classmethod
    def validate_birth_date(cls, v):
        try:
            date_object = datetime.strptime(v, "%d-%m-%Y").date()
        except Exception:
            raise ValueError(
                "La fecha de nacimiento debe estar escrita en formato dd-mm-yyyy"
            )
        return date_object

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        valid_genders = ["Masculino", "Femenino", "No binario", "Prefiero no decir"]
        if v not in valid_genders:
            raise ValueError(
                f'El género debe ser uno de los siguientes: {", ".join(valid_genders)}'
            )
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        import re

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError("Formato de correo electrónico inválido")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v.isnumeric():
            raise ValueError("El número de teléfono debe ser un número")
        if len(v) != 10:
            raise ValueError("El número de teléfono debe tener 10 caracteres")
        return v

    @field_validator("documentId")
    @classmethod
    def validate_document_id(cls, v):
        if not v.isnumeric():
            raise ValueError("El número de documento debe ser un número")
        if len(v) > 10:
            raise ValueError(
                "El número de documento no puede tener más de 10 caracteres"
            )
        return v

    @field_validator("documentType")
    @classmethod
    def validate_document_type(cls, v):
        valid_document_types = ["Tarjeta de identidad", "Cédula"]
        if v not in valid_document_types:
            raise ValueError(
                f'El tipo de documento debe ser uno de los siguientes: {", ".join(valid_document_types)}'
            )
        return v
