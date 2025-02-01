from fastapi import HTTPException, status, UploadFile
from app.core.supabase import supabase
from app.schemas.content import ContentCreate, ContentUpdate
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import uuid
from math import ceil

class ContentService:
    @staticmethod
    async def create_content(content_data: ContentCreate, user_id: str) -> Dict[str, Any]:
        try:
            data = {
                "user_id": user_id,
                "title": content_data.title,
                "description": content_data.description,
                "content_text": content_data.content_text,
                "image_url": str(content_data.image_url) if content_data.image_url else None
            }
            
            response = supabase.table("content").insert(data).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_contents(*args) -> List[Dict[str, Any]]:
        try:
            # Get content with categories and tags
            response = supabase.table("content")\
                .select(
                    "*," +
                    "content_categories(category:categories(*))" +
                    ",content_tags(tag:tags(*))"
                )\
                .execute()

            # Transform the response to match our schema
            for content in response.data:
                # Transform categories
                categories = []
                if "content_categories" in content:
                    for cat in content["content_categories"]:
                        if cat["category"]:
                            categories.append(cat["category"])
                content["categories"] = categories
                del content["content_categories"]

                # Transform tags
                tags = []
                if "content_tags" in content:
                    for tag in content["content_tags"]:
                        if tag["tag"]:
                            tags.append(tag["tag"])
                content["tags"] = tags
                del content["content_tags"]

            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_content(content_id: UUID) -> Dict[str, Any]:
        try:
            response = supabase.table("content")\
                .select(
                    "*," +
                    "content_categories(category:categories(*))" +
                    ",content_tags(tag:tags(*))"
                )\
                .eq("id", str(content_id))\
                .execute()
            
            if not response.data:
                raise HTTPException(status_code=404, detail="Content not found")

            content = response.data[0]
            
            # Transform categories
            categories = []
            if "content_categories" in content:
                for cat in content["content_categories"]:
                    if cat["category"]:
                        categories.append(cat["category"])
            content["categories"] = categories
            del content["content_categories"]

            # Transform tags
            tags = []
            if "content_tags" in content:
                for tag in content["content_tags"]:
                    if tag["tag"]:
                        tags.append(tag["tag"])
            content["tags"] = tags
            del content["content_tags"]

            return content
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def update_content(content_id: UUID, content_data: ContentUpdate, user_id: str) -> Dict[str, Any]:
        try:
            # Verify ownership
            content = await ContentService.get_content(content_id)
            if content["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to update this content")

            # Update content
            update_data = content_data.model_dump(exclude_unset=True)
            response = supabase.table("content").update(update_data).eq("id", str(content_id)).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def delete_content(content_id: UUID, user_id: str) -> Dict[str, Any]:
        try:
            # Verify ownership
            content = await ContentService.get_content(content_id)
            if content["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to delete this content")

            # Delete content
            response = supabase.table("content").delete().eq("id", str(content_id)).execute()
            return response.data[0]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_contents_by_category(category_id: UUID) -> List[Dict[str, Any]]:
        try:
            response = supabase.table("content")\
                .select(
                    "*," +
                    "content_categories(category:categories(*))" +
                    ",content_tags(tag:tags(*))"
                )\
                .eq("content_categories.category_id", str(category_id))\
                .execute()

            # Transform response (same as get_contents)
            for content in response.data:
                categories = []
                if "content_categories" in content:
                    for cat in content["content_categories"]:
                        if cat["category"]:
                            categories.append(cat["category"])
                content["categories"] = categories
                del content["content_categories"]

                tags = []
                if "content_tags" in content:
                    for tag in content["content_tags"]:
                        if tag["tag"]:
                            tags.append(tag["tag"])
                content["tags"] = tags
                del content["content_tags"]

            return response.data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def get_filtered_contents(
        search: Optional[str] = None,
        category_id: Optional[UUID] = None,
        tag_ids: Optional[List[UUID]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "desc",
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        try:
            # Debug print
            print(f"Filtering with: category={category_id}, tags={tag_ids}, dates={start_date}-{end_date}")

            # Start with base query
            query = supabase.table("content")

            # Join with categories and tags if needed
            if category_id:
                query = query.select(
                    "*",
                    "content_categories!inner(category:categories(*))",
                    "content_tags(tag:tags(*))"
                ).eq("content_categories.category_id", str(category_id))
            elif tag_ids:
                query = query.select(
                    "*",
                    "content_categories(category:categories(*))",
                    "content_tags!inner(tag:tags(*))"
                )
                for tag_id in tag_ids:
                    query = query.eq("content_tags.tag_id", str(tag_id))
            else:
                query = query.select(
                    "*",
                    "content_categories(category:categories(*))",
                    "content_tags(tag:tags(*))"
                )

            # Apply date filters - convert to ISO format without microseconds
            if start_date:
                start_date_str = start_date.replace(microsecond=0).isoformat()
                query = query.gte("created_at", start_date_str)
            if end_date:
                end_date_str = end_date.replace(microsecond=0).isoformat()
                query = query.lte("created_at", end_date_str)

            # Apply text search
            if search:
                search = search.lower()
                query = query.or_(
                    f"title.ilike.%{search}%,"
                    f"description.ilike.%{search}%,"
                    f"content_text.ilike.%{search}%"
                )

            # Apply sorting
            if sort_by:
                order_suffix = ".desc" if sort_order.lower() == "desc" else ".asc"
                if sort_by == "date":
                    query = query.order("created_at" + order_suffix)
                elif sort_by == "title":
                    query = query.order("title" + order_suffix)
            else:
                # Default sorting by created_at desc
                query = query.order("created_at.desc")

            # Debug print
            print("Executing query...")
            
            # Execute query
            response = query.execute()
            
            # Debug print
            print(f"Got {len(response.data)} results")

            # Transform response
            result = []
            for content in response.data:
                # Debug print
                print(f"Processing content {content['id']}")
                
                # Get reactions count
                reactions_query = supabase.table("reactions")\
                    .select("*")\
                    .eq("content_id", content["id"])\
                    .execute()
                
                reactions_count = len(reactions_query.data)

                # Transform categories
                categories = []
                if "content_categories" in content:
                    for cat in content["content_categories"]:
                        if cat.get("category"):
                            categories.append(cat["category"])
                content["categories"] = categories
                del content["content_categories"]

                # Transform tags
                tags = []
                if "content_tags" in content:
                    for tag in content["content_tags"]:
                        if tag.get("tag"):
                            tags.append(tag["tag"])
                content["tags"] = tags
                del content["content_tags"]

                # Add reactions count
                content["reactions_count"] = reactions_count

                result.append(content)

            # Sort by reactions if requested
            if sort_by == "reactions":
                result.sort(
                    key=lambda x: x["reactions_count"],
                    reverse=(sort_order.lower() == "desc")
                )

            # Calculate pagination
            total_count = len(result)
            total_pages = ceil(total_count / size)
            start_idx = (page - 1) * size
            end_idx = start_idx + size
            paginated_results = result[start_idx:end_idx]

            # Debug print
            print(f"Returning {len(paginated_results)} items")

            return {
                "items": paginated_results,
                "total": total_count,
                "page": page,
                "size": size,
                "pages": total_pages
            }

        except Exception as e:
            print(f"Error in get_filtered_contents: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    async def upload_image(file: UploadFile, user_id: str) -> dict:
        try:
            # Generate unique filename
            file_extension = file.filename.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_extension}"
            
            # Upload to Supabase storage
            file_path = f"{user_id}/{file_name}"
            file_bytes = await file.read()
            
            response = supabase.storage\
                .from_("content_images")\
                .upload(
                    path=file_path,
                    file=file_bytes,
                    file_options={"content-type": file.content_type}
                )

            # Get public URL
            public_url = supabase.storage\
                .from_("content_images")\
                .get_public_url(file_path)

            return {
                "file_name": file_name,
                "file_path": file_path,
                "public_url": public_url
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            ) 