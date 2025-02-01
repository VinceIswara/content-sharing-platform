from fastapi import APIRouter, Security, Query, File, UploadFile, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse
from app.services.content import ContentService
from app.core.supabase import supabase
from enum import Enum
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

# Add pagination response model
class PaginatedContentResponse(BaseModel):
    items: List[ContentResponse]
    total: int
    page: int
    size: int
    pages: int

# Add sorting enums
class SortField(str, Enum):
    DATE = "date"
    TITLE = "title"
    REACTIONS = "reactions"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

@router.get("/filter", response_model=PaginatedContentResponse)
async def get_filtered_contents(
    search: Optional[str] = Query(None, description="Search in title and description"),
    category_id: Optional[UUID] = Query(None, description="Filter by category ID"),
    tag_ids: Optional[List[UUID]] = Query(None, description="Filter by tag IDs"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    sort_by: Optional[SortField] = Query(None, description="Sort by field"),
    sort_order: Optional[SortOrder] = Query(SortOrder.DESC, description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await ContentService.get_filtered_contents(
        search=search,
        category_id=category_id,
        tag_ids=tag_ids,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        size=size
    )

@router.post("/", response_model=ContentResponse)
async def create_content(
    content: ContentCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ContentService.create_content(content, user.user.id)

@router.get("/", response_model=List[ContentResponse])
async def get_contents(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await ContentService.get_contents()

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await ContentService.get_content(content_id)

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: UUID,
    content: ContentUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ContentService.update_content(content_id, content, user.user.id)

@router.delete("/{content_id}", response_model=ContentResponse)
async def delete_content(
    content_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ContentService.delete_content(content_id, user.user.id)

@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ContentService.upload_image(file, user.user.id) 