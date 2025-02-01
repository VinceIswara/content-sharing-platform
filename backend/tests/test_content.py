from fastapi.testclient import TestClient
import os
from uuid import UUID
from datetime import datetime, timezone, timedelta
import pytest
import time

def test_create_content(client: TestClient, auth_headers):
    response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content",
            "description": "Test Description",
            "content_text": "Test content text"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()
    return response.json()["id"]  # Return the content ID

def test_get_contents(client: TestClient, auth_headers):
    response = client.get(
        "/api/v1/content/",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_content(client: TestClient, auth_headers):
    # First create content
    response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content",
            "description": "Test Description",
            "content_text": "Test content text"
        }
    )
    content_id = response.json()["id"]

    # Then update it
    response = client.put(
        f"/api/v1/content/{content_id}",
        headers=auth_headers,
        json={
            "title": "Updated Title",
            "description": "Updated Description",
            "content_text": "Updated content text"
        }
    )
    assert response.status_code == 200

def test_delete_content(client: TestClient, auth_headers):
    # First create content
    response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content",
            "description": "Test Description",
            "content_text": "Test content text"
        }
    )
    content_id = response.json()["id"]

    # Then delete it
    response = client.delete(
        f"/api/v1/content/{content_id}",
        headers=auth_headers
    )
    assert response.status_code == 200

def test_upload_image(client: TestClient, auth_headers):
    # Create a small test image
    test_image_path = "tests/test_image.jpg"
    with open(test_image_path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)  # Minimal valid PNG file

    try:
        # Upload image
        with open(test_image_path, "rb") as f:
            response = client.post(
                "/api/v1/content/upload-image",
                headers=auth_headers,
                files={"file": ("test_image.jpg", f, "image/jpeg")}
            )
        
        assert response.status_code == 200
        assert "public_url" in response.json()
        assert "file_path" in response.json()
        
    finally:
        # Clean up test file
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

def test_filter_by_category(client, auth_headers):
    # Create unique category name using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    category_name = f"Test Category {timestamp}"
    
    # First create a category
    category_response = client.post(
        "/api/v1/categories/",
        headers=auth_headers,
        json={
            "name": category_name,
            "description": "Test category for filtering"
        }
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    # Create content with category
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content with Category",
            "description": "Testing category filter",
            "content_text": "This content has a category"
        }
    )
    assert content_response.status_code == 200
    content_id = content_response.json()["id"]

    # Add category to content
    add_category_response = client.post(
        "/api/v1/categories/content-categories",
        headers=auth_headers,
        json={
            "content_id": str(content_id),
            "category_ids": [str(category_id)]
        }
    )
    assert add_category_response.status_code == 200

    # Wait for data to be saved
    time.sleep(1)

    # Test filtering by category
    filter_response = client.get(
        f"/api/v1/content/filter?category_id={category_id}",
        headers=auth_headers
    )
    assert filter_response.status_code == 200
    filtered_content = filter_response.json()
    assert len(filtered_content["items"]) > 0
    assert any(str(content["id"]) == str(content_id) for content in filtered_content["items"])

def test_filter_by_tag(client, auth_headers):
    # Create unique tag name using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    tag_name = f"test-tag-{timestamp}"
    
    # First create a tag
    tag_response = client.post(
        "/api/v1/tags/",
        headers=auth_headers,
        json={
            "name": tag_name
        }
    )
    assert tag_response.status_code == 200
    tag_id = tag_response.json()["id"]

    # Create content
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content with Tag",
            "description": "Testing tag filter",
            "content_text": "This content has a tag"
        }
    )
    assert content_response.status_code == 200
    content_id = content_response.json()["id"]

    # Add tag to content
    add_tag_response = client.post(
        "/api/v1/tags/content-tags",
        headers=auth_headers,
        json={
            "content_id": str(content_id),
            "tag_ids": [str(tag_id)]
        }
    )
    assert add_tag_response.status_code == 200

    # Wait for data to be saved
    time.sleep(1)

    # Test filtering by tag
    filter_response = client.get(
        f"/api/v1/content/filter?tag_ids={tag_id}",
        headers=auth_headers
    )
    assert filter_response.status_code == 200
    filtered_content = filter_response.json()
    assert len(filtered_content["items"]) > 0
    assert any(str(content["id"]) == str(content_id) for content in filtered_content["items"])

def test_filter_by_date(client, auth_headers):
    # Create content
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content for Date Filter",
            "description": "Testing date filter",
            "content_text": "This content will be filtered by date"
        }
    )
    assert content_response.status_code == 200
    content_id = content_response.json()["id"]

    # Wait for data to be saved
    time.sleep(1)

    # Use timezone-aware datetime with Z suffix for UTC
    now = datetime.now(timezone.utc)
    start_date = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_date = (now + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Test filtering by date range
    filter_response = client.get(
        f"/api/v1/content/filter?start_date={start_date}&end_date={end_date}",
        headers=auth_headers
    )
    assert filter_response.status_code == 200
    filtered_content = filter_response.json()
    assert len(filtered_content["items"]) > 0
    assert any(str(content["id"]) == str(content_id) for content in filtered_content["items"])

def test_combined_filters(client, auth_headers):
    # Create unique names using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    category_name = f"Combined Test Category {timestamp}"
    tag_name = f"combined-test-tag-{timestamp}"
    
    # Create category and tag
    category_response = client.post(
        "/api/v1/categories/",
        headers=auth_headers,
        json={
            "name": category_name,
            "description": "Test category for combined filtering"
        }
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    tag_response = client.post(
        "/api/v1/tags/",
        headers=auth_headers,
        json={
            "name": tag_name
        }
    )
    assert tag_response.status_code == 200
    tag_id = tag_response.json()["id"]

    # Create content
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Combined Filters",
            "description": "Testing combined filters",
            "content_text": "This content has both category and tag"
        }
    )
    assert content_response.status_code == 200
    content_id = content_response.json()["id"]

    # Add category and tag
    client.post(
        "/api/v1/categories/content-categories",
        headers=auth_headers,
        json={
            "content_id": str(content_id),
            "category_ids": [str(category_id)]
        }
    )
    client.post(
        "/api/v1/tags/content-tags",
        headers=auth_headers,
        json={
            "content_id": str(content_id),
            "tag_ids": [str(tag_id)]
        }
    )

    # Wait for data to be saved
    time.sleep(1)

    # Test combined filtering
    filter_response = client.get(
        f"/api/v1/content/filter?category_id={category_id}&tag_ids={tag_id}",
        headers=auth_headers
    )
    assert filter_response.status_code == 200
    filtered_content = filter_response.json()
    assert len(filtered_content["items"]) > 0
    assert any(str(content["id"]) == str(content_id) for content in filtered_content["items"]) 