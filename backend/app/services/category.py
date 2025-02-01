from fastapi import HTTPException, status
from app.core.supabase import supabase
from app.schemas.category import CategoryCreate, CategoryUpdate, ContentCategoryCreate
from typing import List, Dict, Any
from uuid import UUID

class CategoryService:
    @staticmethod
    async def create_category(category_data: CategoryCreate) -> Dict[str, Any]:
        try:
            response = supabase.table("categories").insert(category_data.model_dump()).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_categories() -> List[Dict[str, Any]]:
        try:
            response = supabase.table("categories").select("*").execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_category(category_id: UUID) -> Dict[str, Any]:
        try:
            response = supabase.table("categories")\
                .select("*")\
                .eq("id", str(category_id))\
                .execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="Category not found")
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def update_category(category_id: UUID, category_data: CategoryUpdate) -> Dict[str, Any]:
        try:
            response = supabase.table("categories")\
                .update(category_data.model_dump())\
                .eq("id", str(category_id))\
                .execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="Category not found")
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def delete_category(category_id: UUID) -> Dict[str, Any]:
        try:
            response = supabase.table("categories")\
                .delete()\
                .eq("id", str(category_id))\
                .execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="Category not found")
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def add_content_categories(content_categories: ContentCategoryCreate) -> List[Dict[str, Any]]:
        try:
            data = [
                {"content_id": str(content_categories.content_id), "category_id": str(cat_id)}
                for cat_id in content_categories.category_ids
            ]
            response = supabase.table("content_categories").insert(data).execute()
            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) 