from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas.reaction import ReactionCreate, ReactionResponse, ContentReactions, ReactionUpdate
from app.services.reaction import ReactionService
from app.core.supabase import supabase
from typing import List
from uuid import UUID

router = APIRouter()
security = HTTPBearer()

@router.post("/", response_model=ReactionResponse)
async def create_reaction(
    reaction_data: ReactionCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ReactionService.create_reaction(reaction_data, user.user.id)

@router.get("/{content_id}", response_model=ContentReactions)
async def get_content_reactions(
    content_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ReactionService.get_content_reactions(content_id, user.user.id)

@router.delete("/{content_id}")
async def delete_reaction(
    content_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ReactionService.delete_reaction(content_id, user.user.id)

@router.put("/{content_id}", response_model=ReactionResponse)
async def update_reaction(
    content_id: UUID,
    reaction_data: ReactionUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await ReactionService.update_reaction(content_id, reaction_data, user.user.id) 