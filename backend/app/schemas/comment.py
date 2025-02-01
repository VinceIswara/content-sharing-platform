from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class CommentBase(BaseModel):
    comment_text: str = Field(..., min_length=1, max_length=1000)  # Ensure comment is not empty

class CommentCreate(CommentBase):
    content_id: UUID

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: UUID
    content_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 