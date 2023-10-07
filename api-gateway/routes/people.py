from json.decoder import JSONDecodeError

from fastapi import APIRouter, Request
from starlette import status

from core.people_service.factory import get_people_service

people_router = APIRouter()
people_service = get_people_service()


@people_router.get("/")
async def list(request: Request):
    query_params = dict(request.query_params)
    response = people_service.list(query_params)
    return response


@people_router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: Request):
    try:
        body = await request.json()
        response = people_service.create(body)
        return response
    except JSONDecodeError:
        return {"message": "Invalid JSON body."}


@people_router.patch("/{documentId}")
async def update(request: Request, documentId: str):
    try:
        body = await request.json()
        response = people_service.update(documentId, body)
        return response
    except JSONDecodeError:
        return {"message": "Invalid JSON body."}


@people_router.get("/{documentId}")
async def detail(documentId: str):
    response = people_service.detail(documentId)
    return response


@people_router.delete("/{documentId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(documentId: str):
    people_service.delete(documentId)
