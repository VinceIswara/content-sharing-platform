from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, ContentCategoryCreate
from app.services.category import CategoryService
from typing import List
from uuid import UUID

router = APIRouter()
security = HTTPBearer()

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CategoryService.create_category(category_data)

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CategoryService.get_categories()

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CategoryService.get_category(category_id)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CategoryService.update_category(category_id, category_data)

@router.delete("/{category_id}", response_model=CategoryResponse)
async def delete_category(
    category_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CategoryService.delete_category(category_id)

@router.post("/content-categories", response_model=List[dict])
async def add_content_categories(
    content_categories: ContentCategoryCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CategoryService.add_content_categories(content_categories) 