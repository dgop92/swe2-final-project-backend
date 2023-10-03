from typing import List

from core.people_service.definitions import (
    PeopleBody,
    PeopleQuery,
    PeopleResponse,
    PeopleService,
)


class FakePeopleService(PeopleService):
    def __init__(self) -> None:
        super().__init__()

    def create(self, body: PeopleBody) -> PeopleResponse:
        return {"id": "1", "name": "John Doe", "age": 30}

    def update(self, id: str, body: PeopleBody) -> PeopleResponse:
        return {"id": id, "name": "John Doe", "age": 30}

    def detail(self, id: str) -> PeopleResponse:
        return {"id": id, "name": "John Doe", "age": 30}

    def delete(self, id: str) -> PeopleResponse:
        return {}

    def list(self, query: PeopleQuery) -> List[PeopleResponse]:
        return [{"id": "1", "name": "John Doe", "age": 30}]
