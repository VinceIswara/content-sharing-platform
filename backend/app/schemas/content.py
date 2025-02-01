from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .category import CategoryResponse
from .tag import TagResponse

class ContentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Optional[str] = None
    content_text: str
    image_url: Optional[HttpUrl] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_text: Optional[str] = None
    image_url: Optional[HttpUrl] = None

class ContentResponse(ContentBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    categories: Optional[List[CategoryResponse]] = None
    tags: Optional[List[TagResponse]] = None 