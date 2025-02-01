from fastapi import APIRouter, HTTPException
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth import AuthService

router = APIRouter()

@router.post("/signup", response_model=Token)
async def sign_up(user_data: UserCreate):
    response = await AuthService.sign_up(user_data)
    if response.session:
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=400, detail="Sign up failed")

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    response = await AuthService.sign_in(user_data)
    if response.session:
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }
    raise HTTPException(status_code=400, detail="Login failed") 