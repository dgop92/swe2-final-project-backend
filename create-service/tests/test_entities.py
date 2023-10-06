from datetime import date

import pytest

from core.entities import People


def test_valid_person():
    person = People(
        documentType="Cédula",
        documentId="1234567890",
        firstName="John",
        middleName="Doe",
        lastName="Smith",
        birthDate="01-05-1990",
        gender="Masculino",
        email="johndoe@example.com",
        phone="1234567890",
    )
    assert person.documentType == "Cédula"
    assert person.documentId == "1234567890"
    assert person.firstName == "John"
    assert person.middleName == "Doe"
    assert person.lastName == "Smith"
    assert person.birthDate == date(1990, 5, 1)
    assert person.gender == "Masculino"
    assert person.email == "johndoe@example.com"
    assert person.phone == "1234567890"


def test_invalid_first_name():
    with pytest.raises(ValueError, match="El primer nombre no puede ser un número"):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="123",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )


def test_invalid_middle_name():
    with pytest.raises(
        ValueError, match="El segundo nombre no puede tener más de 30 caracteres"
    ):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="John",
            middleName="DoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoeDoe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )


def test_invalid_last_name():
    with pytest.raises(ValueError, match="El apellido no puede ser un número"):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="John",
            middleName="Doe",
            lastName="123",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )


def test_invalid_birth_date():
    with pytest.raises(
        ValueError,
        match="La fecha de nacimiento debe estar escrita en formato dd-mm-yyyy",
    ):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="1990-02-05",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )


def test_invalid_gender():
    with pytest.raises(
        ValueError,
        match="El género debe ser uno de los siguientes: Masculino, Femenino, No binario, Prefiero no decir",
    ):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Otro",
            email="johndoe@example.com",
            phone="1234567890",
        )


def test_invalid_email():
    with pytest.raises(ValueError, match="Formato de correo electrónico inválido"):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoeexample.com",
            phone="1234567890",
        )


def test_invalid_phone():
    with pytest.raises(
        ValueError, match="El número de teléfono debe tener 10 caracteres"
    ):
        People(
            documentType="Cédula",
            documentId="1234567890",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="123456789",
        )


def test_invalid_document_id():
    with pytest.raises(
        ValueError, match="El número de documento no puede tener más de 10 caracteres"
    ):
        People(
            documentType="Cédula",
            documentId="12345678900",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )

    with pytest.raises(ValueError, match="El número de documento debe ser un número"):
        People(
            documentType="Cédula",
            documentId="1234sad",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )


def test_invalid_document_type():
    with pytest.raises(
        ValueError,
        match="El tipo de documento debe ser uno de los siguientes: Tarjeta de identidad, Cédula",
    ):
        People(
            documentType="Pasaporte",
            documentId="1234567890",
            firstName="John",
            middleName="Doe",
            lastName="Smith",
            birthDate="01-05-1990",
            gender="Masculino",
            email="johndoe@example.com",
            phone="1234567890",
        )
