from fastapi import HTTPException, status
from app.core.supabase import supabase
from app.schemas.reaction import ReactionCreate, ReactionUpdate, ReactionType
from typing import List, Dict, Any, Optional
from uuid import UUID

class ReactionService:
    @staticmethod
    async def create_reaction(reaction_data: ReactionCreate, user_id: str) -> Dict[str, Any]:
        try:
            data = {
                "content_id": str(reaction_data.content_id),
                "user_id": user_id,
                "reaction_type": reaction_data.reaction_type.value
            }
            
            response = supabase.table("reactions").upsert(data).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_content_reactions(content_id: UUID, user_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Get all reactions for the content
            response = supabase.table("reactions")\
                .select("reaction_type")\
                .eq("content_id", str(content_id))\
                .execute()
            
            # Count reactions manually
            counts = {}
            for reaction in response.data:
                rt = reaction['reaction_type']
                counts[rt] = counts.get(rt, 0) + 1
            
            # Get user's reaction if user_id provided
            user_reaction = None
            if user_id:
                user_response = supabase.table("reactions")\
                    .select("reaction_type")\
                    .eq("content_id", str(content_id))\
                    .eq("user_id", user_id)\
                    .execute()
                if user_response.data:
                    user_reaction = user_response.data[0]['reaction_type']
            
            return {
                "content_id": str(content_id),
                "reactions": [
                    {"reaction_type": rt.value, "count": counts.get(rt.value, 0)}
                    for rt in ReactionType
                ],
                "user_reaction": user_reaction
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def delete_reaction(content_id: UUID, user_id: str) -> Dict[str, Any]:
        try:
            response = supabase.table("reactions")\
                .delete()\
                .eq("content_id", str(content_id))\
                .eq("user_id", user_id)\
                .execute()
            return response.data[0] if response.data else {"message": "Reaction removed"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def update_reaction(content_id: UUID, reaction_data: ReactionUpdate, user_id: str) -> Dict[str, Any]:
        try:
            response = supabase.table("reactions")\
                .update({"reaction_type": reaction_data.reaction_type.value})\
                .eq("content_id", str(content_id))\
                .eq("user_id", user_id)\
                .execute()
            
            if not response.data:
                raise HTTPException(status_code=404, detail="Reaction not found")
            
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) 