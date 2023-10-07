import logging
from typing import Union

from config.settings import PEOPLE_SERVICE_TYPE
from core.people_service.definitions import PeopleService
from core.people_service.fake_people_service import FakePeopleService
from core.people_service.rest_people_service import RestPeopleService

people_service: Union[PeopleService, None] = None


logger = logging.getLogger(__name__)


def create_people_service(service_type: str):
    global people_service
    if service_type == "fake":
        if not people_service:
            logger.info("people_service is not initialized, creating a new one.")
            people_service = FakePeopleService()
        return people_service
    elif service_type == "rest":
        if not people_service:
            logger.info("people_service is not initialized, creating a new one.")
            people_service = RestPeopleService()
        return people_service

    raise Exception("Invalid service type.")


def get_people_service():
    return create_people_service(PEOPLE_SERVICE_TYPE)
