from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ReactionType(str, Enum):
    LIKE = 'like'
    LOVE = 'love'
    LAUGH = 'laugh'
    WOW = 'wow'
    SAD = 'sad'
    ANGRY = 'angry'

class ReactionCreate(BaseModel):
    content_id: UUID
    reaction_type: ReactionType

class ReactionUpdate(BaseModel):
    reaction_type: ReactionType

class ReactionResponse(BaseModel):
    id: UUID
    content_id: UUID
    user_id: UUID
    reaction_type: ReactionType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReactionCount(BaseModel):
    reaction_type: ReactionType
    count: int

class ContentReactions(BaseModel):
    content_id: UUID
    reactions: List[ReactionCount]
    user_reaction: Optional[ReactionType] = None 