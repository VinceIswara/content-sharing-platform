from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ContentCategoryCreate(BaseModel):
    content_id: UUID
    category_ids: List[UUID] 