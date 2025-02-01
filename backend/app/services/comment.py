from fastapi import HTTPException, status
from app.core.supabase import supabase
from app.schemas.comment import CommentCreate, CommentUpdate
from typing import List, Dict, Any
from uuid import UUID

class CommentService:
    @staticmethod
    async def create_comment(comment_data: CommentCreate, user_id: str) -> Dict[str, Any]:
        try:
            data = {
                "content_id": str(comment_data.content_id),
                "user_id": user_id,
                "comment_text": comment_data.comment_text
            }
            
            response = supabase.table("comments").insert(data).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_comments(content_id: UUID) -> List[Dict[str, Any]]:
        try:
            response = supabase.table("comments")\
                .select("*")\
                .eq("content_id", str(content_id))\
                .execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def update_comment(comment_id: UUID, comment_data: CommentUpdate, user_id: str) -> Dict[str, Any]:
        try:
            # Verify ownership
            comment = supabase.table("comments")\
                .select("*")\
                .eq("id", str(comment_id))\
                .execute()
            
            if not comment.data or comment.data[0]["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this comment")

            response = supabase.table("comments")\
                .update({"comment_text": comment_data.comment_text})\
                .eq("id", str(comment_id))\
                .execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def delete_comment(comment_id: UUID, user_id: str) -> Dict[str, Any]:
        try:
            # Verify ownership
            comment = supabase.table("comments")\
                .select("*")\
                .eq("id", str(comment_id))\
                .execute()
            
            if not comment.data or comment.data[0]["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

            response = supabase.table("comments")\
                .delete()\
                .eq("id", str(comment_id))\
                .execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) 