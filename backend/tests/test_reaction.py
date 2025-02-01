from fastapi.testclient import TestClient
from uuid import UUID

def test_reaction_workflow(client: TestClient, auth_headers):
    # First create content to react to
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content for Reactions",
            "description": "Testing reactions",
            "content_text": "This content will receive reactions"
        }
    )
    assert content_response.status_code == 200
    content_id = content_response.json()["id"]

    # Test creating a reaction
    reaction_response = client.post(
        "/api/v1/reactions/",
        headers=auth_headers,
        json={
            "content_id": content_id,
            "reaction_type": "love"
        }
    )
    assert reaction_response.status_code == 200
    assert reaction_response.json()["reaction_type"] == "love"

    # Test getting reactions
    get_response = client.get(
        f"/api/v1/reactions/{content_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 200
    assert get_response.json()["user_reaction"] == "love"
    assert any(r["reaction_type"] == "love" and r["count"] == 1 
              for r in get_response.json()["reactions"])

    # Test updating reaction
    update_response = client.put(
        f"/api/v1/reactions/{content_id}",
        headers=auth_headers,
        json={
            "reaction_type": "wow"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["reaction_type"] == "wow"

    # Verify update
    get_response = client.get(
        f"/api/v1/reactions/{content_id}",
        headers=auth_headers
    )
    assert get_response.json()["user_reaction"] == "wow"

    # Test deleting reaction
    delete_response = client.delete(
        f"/api/v1/reactions/{content_id}",
        headers=auth_headers
    )
    assert delete_response.status_code == 200

    # Verify deletion
    get_response = client.get(
        f"/api/v1/reactions/{content_id}",
        headers=auth_headers
    )
    assert get_response.json()["user_reaction"] is None
    assert all(r["count"] == 0 for r in get_response.json()["reactions"])

def test_invalid_reaction_type(client: TestClient, auth_headers):
    # Create content
    content_response = client.post(
        "/api/v1/content/",
        headers=auth_headers,
        json={
            "title": "Test Content for Invalid Reaction",
            "description": "Testing invalid reaction",
            "content_text": "This content will test invalid reactions"
        }
    )
    content_id = content_response.json()["id"]

    # Test invalid reaction type
    response = client.post(
        "/api/v1/reactions/",
        headers=auth_headers,
        json={
            "content_id": content_id,
            "reaction_type": "invalid_type"
        }
    )
    assert response.status_code == 422  # Validation error

def test_reaction_to_nonexistent_content(client: TestClient, auth_headers):
    # Test reaction to non-existent content
    response = client.post(
        "/api/v1/reactions/",
        headers=auth_headers,
        json={
            "content_id": "123e4567-e89b-12d3-a456-426614174000",
            "reaction_type": "like"
        }
    )
    assert response.status_code == 400  # Bad request 