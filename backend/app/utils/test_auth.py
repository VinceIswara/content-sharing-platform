from fastapi.testclient import TestClient
from app.core.supabase import supabase
from typing import Dict

class TestAuth:
    @staticmethod
    def get_test_token() -> Dict[str, str]:
        """Get a reusable test token"""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": "leluminaty@gmail.com",  # Use your existing test account
                "password": "1Dontknow!"      # Use your actual password
            })
            return {
                "Authorization": f"Bearer {response.session.access_token}"
            }
        except Exception as e:
            print(f"Auth error: {e}")
            return {} 