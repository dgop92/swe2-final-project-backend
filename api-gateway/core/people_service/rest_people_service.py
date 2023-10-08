from typing import List

import requests
from fastapi import HTTPException, UploadFile

from config.settings import PEOPLE_SERVICE_URLS
from core.people_service.definitions import (
    PeopleBody,
    PeopleQuery,
    PeopleResponse,
    PeopleService,
)


def upload_image(document_id: str, upload_file: UploadFile):
    files = {"file": (upload_file.filename, upload_file.file, upload_file.content_type)}
    r = requests.patch(
        f"{PEOPLE_SERVICE_URLS['update']}/update/{document_id}/image",
        files=files,
        timeout=15,
    )
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 422:
        raise HTTPException(status_code=422, detail=r.json()["detail"])
    elif r.status_code == 404:
        raise HTTPException(status_code=404, detail=r.json()["detail"])
    elif r.status_code == 400:
        raise HTTPException(status_code=400, detail=r.json()["detail"])
    else:
        raise HTTPException(status_code=500)


class RestPeopleService(PeopleService):
    def __init__(self) -> None:
        super().__init__()

    def create(self, body: PeopleBody) -> PeopleResponse:
        r = requests.post(
            f"{PEOPLE_SERVICE_URLS['create']}/create", json=body, timeout=15
        )

        if r.status_code == 201:
            return r.json()
        elif r.status_code == 422:
            raise HTTPException(status_code=422, detail=r.json()["detail"])
        elif r.status_code == 400:
            raise HTTPException(status_code=400, detail=r.json()["detail"])
        else:
            raise HTTPException(status_code=500)

    def update(self, id: str, body: PeopleBody) -> PeopleResponse:
        r = requests.patch(
            f"{PEOPLE_SERVICE_URLS['update']}/update/{id}", json=body, timeout=15
        )

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 422:
            raise HTTPException(status_code=422, detail=r.json()["detail"])
        elif r.status_code == 400:
            raise HTTPException(status_code=400, detail=r.json()["detail"])
        elif r.status_code == 404:
            raise HTTPException(status_code=404, detail=r.json()["detail"])
        else:
            raise HTTPException(status_code=500)

    def detail(self, id: str) -> PeopleResponse:
        r = requests.get(f"{PEOPLE_SERVICE_URLS['read']}/detail/{id}", timeout=15)

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            raise HTTPException(status_code=404, detail=r.json()["detail"])
        else:
            raise HTTPException(status_code=500)

    def delete(self, id: str) -> PeopleResponse:
        r = requests.delete(f"{PEOPLE_SERVICE_URLS['delete']}/delete/{id}", timeout=15)

        if r.status_code == 204:
            return {}
        elif r.status_code == 404:
            raise HTTPException(status_code=404, detail=r.json()["detail"])
        else:
            raise HTTPException(status_code=500)

    def list(self, query: PeopleQuery) -> List[PeopleResponse]:
        return [{"id": "1", "name": "John Doe", "age": 30}]
