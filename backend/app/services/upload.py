from fastapi import UploadFile, HTTPException
from app.core.supabase import supabase
import uuid

class UploadService:
    @staticmethod
    async def upload_image(file: UploadFile, user_id: str) -> str:
        try:
            # Generate unique filename
            file_ext = file.filename.split('.')[-1]
            unique_filename = f"{user_id}/{uuid.uuid4()}.{file_ext}"
            
            # Upload to Supabase Storage
            response = supabase.storage.from_('content_images').upload(
                unique_filename,
                file.file.read()
            )
            
            # Get public URL
            public_url = supabase.storage.from_('content_images').get_public_url(unique_filename)
            return public_url
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 