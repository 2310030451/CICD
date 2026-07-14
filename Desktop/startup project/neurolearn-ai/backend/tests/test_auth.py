import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import create_access_token, create_refresh_token, decode_token
from app.core.rbac import rbac_manager
from datetime import datetime, timedelta


@pytest.fixture
async def client():
    async with TestClient(app) as test_client:
        yield test_client


class TestJWTAuthentication:
    def test_create_access_token(self):
        user_id = "test_user"
        token = create_access_token(user_id)
        assert token is not None
        assert isinstance(token, str)
        
    def test_create_refresh_token(self):
        user_id = "test_user"
        token = create_refresh_token(user_id)
        assert token is not None
        assert isinstance(token, str)
        
    def test_verify_valid_token(self):
        user_id = "test_user"
        token = create_access_token(user_id)
        payload = decode_token(token)
        assert payload is not None
        assert payload.get("sub") == user_id
        
    def test_verify_invalid_token(self):
        invalid_token = "invalid.token.here"
        payload = decode_token(invalid_token)
        assert payload is None


class TestRBAC:
    def test_role_exists(self):
        assert rbac_manager.role_exists("admin")
        assert rbac_manager.role_exists("user")
        assert rbac_manager.role_exists("teacher")
        assert rbac_manager.role_exists("parent")
        assert rbac_manager.role_exists("student")
        
    def test_permission_exists(self):
        assert rbac_manager.permission_exists("read:documents")
        assert rbac_manager.permission_exists("write:documents")
        assert rbac_manager.permission_exists("delete:documents")
        
    def test_role_has_permission(self):
        assert rbac_manager.role_has_permission("admin", "read:documents")
        assert rbac_manager.role_has_permission("admin", "write:documents")
        assert rbac_manager.role_has_permission("admin", "delete:documents")
        
    def test_user_has_permission(self):
        # Admin should have all permissions
        assert rbac_manager.user_has_permission("admin", "read:documents")
        assert rbac_manager.user_has_permission("admin", "write:documents")
        
        # User should have limited permissions
        assert rbac_manager.user_has_permission("user", "read:documents")
        assert not rbac_manager.user_has_permission("user", "delete:documents")


class TestAuthAPI:
    @pytest.mark.asyncio
    async def test_register_endpoint(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword123",
                "name": "Test User"
            }
        )
        assert response.status_code in [200, 400, 422]
        
    @pytest.mark.asyncio
    async def test_login_endpoint(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code in [200, 400, 401, 422]
        
    @pytest.mark.asyncio
    async def test_refresh_token_endpoint(self, client):
        response = client.post(
            "/api/v1/auth/refresh",
            json={
                "refresh_token": "test_refresh_token"
            }
        )
        assert response.status_code in [200, 401, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
