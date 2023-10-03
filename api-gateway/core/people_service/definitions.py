from abc import ABC
from typing import Any, Dict, List

PeopleResponse = Dict[str, Any]
PeopleBody = Dict[str, Any]
PeopleQuery = Dict[str, Any]


# abstract class
class PeopleService(ABC):
    def create(self, body: PeopleBody) -> PeopleResponse:
        raise NotImplementedError

    def update(self, id: str, body: PeopleBody) -> PeopleResponse:
        raise NotImplementedError

    def detail(self, id: str) -> PeopleResponse:
        raise NotImplementedError

    def delete(self, id: str) -> PeopleResponse:
        raise NotImplementedError

    def list(self, query: PeopleQuery) -> List[PeopleResponse]:
        raise NotImplementedError
