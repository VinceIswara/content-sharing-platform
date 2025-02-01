from fastapi.testclient import TestClient
from uuid import UUID

def test_comment_workflow(client: TestClient, auth_headers):
    # First create content to comment on
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content for Comments",
            "description": "Testing comments",
            "content_text": "This content will receive comments"
        }
    )
    assert content_response.status_code == 200
    content_id = content_response.json()["id"]

    # Test creating a comment
    comment_response = client.post(
        "/api/v1/comments/",
        headers=auth_headers,
        json={
            "content_id": content_id,
            "comment_text": "This is a test comment!"
        }
    )
    assert comment_response.status_code == 200
    assert comment_response.json()["comment_text"] == "This is a test comment!"
    comment_id = comment_response.json()["id"]

    # Test getting comments for content
    get_response = client.get(
        f"/api/v1/comments/{content_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 200
    assert len(get_response.json()) > 0
    assert any(comment["comment_text"] == "This is a test comment!" 
              for comment in get_response.json())

    # Test updating comment
    update_response = client.put(
        f"/api/v1/comments/{comment_id}",
        headers=auth_headers,
        json={
            "comment_text": "This comment has been updated!"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["comment_text"] == "This comment has been updated!"

    # Verify update
    get_response = client.get(
        f"/api/v1/comments/{content_id}",
        headers=auth_headers
    )
    assert any(comment["comment_text"] == "This comment has been updated!" 
              for comment in get_response.json())

    # Test deleting comment
    delete_response = client.delete(
        f"/api/v1/comments/{comment_id}",
        headers=auth_headers
    )
    assert delete_response.status_code == 200

    # Verify deletion
    get_response = client.get(
        f"/api/v1/comments/{content_id}",
        headers=auth_headers
    )
    assert not any(comment["id"] == comment_id 
                  for comment in get_response.json())

def test_comment_on_nonexistent_content(client: TestClient, auth_headers):
    # Test commenting on non-existent content
    response = client.post(
        "/api/v1/comments/",
        headers=auth_headers,
        json={
            "content_id": "123e4567-e89b-12d3-a456-426614174000",
            "comment_text": "This comment should fail"
        }
    )
    assert response.status_code == 400  # Bad request

def test_empty_comment(client: TestClient, auth_headers):
    # Create content first
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content for Empty Comment",
            "description": "Testing empty comment",
            "content_text": "This content will test empty comments"
        }
    )
    content_id = content_response.json()["id"]

    # Test empty comment
    response = client.post(
        "/api/v1/comments/",
        headers=auth_headers,
        json={
            "content_id": content_id,
            "comment_text": ""
        }
    )
    assert response.status_code == 422  # Validation error 