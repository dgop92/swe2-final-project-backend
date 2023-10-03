import logging
from typing import Union

from core.people_service.definitions import PeopleService
from core.people_service.fake_people_service import FakePeopleService

people_service: Union[PeopleService, None] = None


logger = logging.getLogger(__name__)


def create_people_service(service_type: str):
    if service_type == "fake":
        global people_service
        if not people_service:
            logger.info("people_service is not initialized, creating a new one.")
            people_service = FakePeopleService()
        return people_service

    raise Exception("Invalid service type.")


def get_people_service():
    return create_people_service("fake")
