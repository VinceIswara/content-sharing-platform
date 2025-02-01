from fastapi import HTTPException, status
from app.core.supabase import supabase
from app.schemas.auth import UserCreate, UserLogin
from typing import Dict, Any

class AuthService:
    @staticmethod
    async def sign_up(user_data: UserCreate) -> Dict[str, Any]:
        try:
            # Sign up user with Supabase
            auth_response = supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
            })
            
            # If signup successful, create user profile
            if auth_response.user:
                # Insert additional user data into profiles table
                profile_data = {
                    "id": auth_response.user.id,
                    "full_name": user_data.full_name,
                    "email": user_data.email
                }
                
                supabase.table("profiles").insert(profile_data).execute()
                
            return auth_response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def sign_in(user_data: UserLogin) -> Dict[str, Any]:
        try:
            response = supabase.auth.sign_in_with_password({
                "email": user_data.email,
                "password": user_data.password
            })
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) 