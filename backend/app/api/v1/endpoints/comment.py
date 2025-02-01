from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.comment import CommentService
from app.core.supabase import supabase
from typing import List
from uuid import UUID

router = APIRouter()
security = HTTPBearer()

@router.post("/", response_model=CommentResponse)
async def create_comment(
    comment_data: CommentCreate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await CommentService.create_comment(comment_data, user.user.id)

@router.get("/{content_id}", response_model=List[CommentResponse])
async def get_comments(
    content_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return await CommentService.get_comments(content_id)

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: UUID,
    comment_data: CommentUpdate,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await CommentService.update_comment(comment_id, comment_data, user.user.id)

@router.delete("/{comment_id}", response_model=CommentResponse)
async def delete_comment(
    comment_id: UUID,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    return await CommentService.delete_comment(comment_id, user.user.id) 