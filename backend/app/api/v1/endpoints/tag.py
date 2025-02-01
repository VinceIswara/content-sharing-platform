from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas.tag import TagCreate, TagResponse, ContentTagCreate
from app.services.tag import TagService
from typing import List
from uuid import UUID

router = APIRouter()
security = HTTPBearer()

@router.post("/", response_model=TagResponse)
async def create_tag(
    tag_data: TagCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await TagService.create_tag(tag_data)

@router.get("/", response_model=List[TagResponse])
async def get_tags(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await TagService.get_tags()

@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await TagService.get_tag(tag_id)

@router.delete("/{tag_id}", response_model=TagResponse)
async def delete_tag(
    tag_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await TagService.delete_tag(tag_id)

@router.post("/content-tags", response_model=List[dict])
async def add_content_tags(
    content_tags: ContentTagCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await TagService.add_content_tags(content_tags) 