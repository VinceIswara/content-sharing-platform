from fastapi import HTTPException, status
from app.core.supabase import supabase
from app.schemas.tag import TagCreate, ContentTagCreate
from typing import List, Dict, Any
from uuid import UUID

class TagService:
    @staticmethod
    async def create_tag(tag_data: TagCreate) -> Dict[str, Any]:
        try:
            response = supabase.table("tags").insert(tag_data.model_dump()).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_tags() -> List[Dict[str, Any]]:
        try:
            response = supabase.table("tags").select("*").execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_tag(tag_id: UUID) -> Dict[str, Any]:
        try:
            response = supabase.table("tags")\
                .select("*")\
                .eq("id", str(tag_id))\
                .execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="Tag not found")
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def delete_tag(tag_id: UUID) -> Dict[str, Any]:
        try:
            response = supabase.table("tags")\
                .delete()\
                .eq("id", str(tag_id))\
                .execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="Tag not found")
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def add_content_tags(content_tags: ContentTagCreate) -> List[Dict[str, Any]]:
        try:
            data = [
                {"content_id": str(content_tags.content_id), "tag_id": str(tag_id)}
                for tag_id in content_tags.tag_ids
            ]
            response = supabase.table("content_tags").insert(data).execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) 