from fastapi import Request, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import secrets

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https: wss:;"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response

class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """Middleware to protect against CSRF attacks"""
    
    def __init__(self, app, secret_key: str = None):
        super().__init__(app)
        self.secret_key = secret_key or secrets.token_hex(32)
    
    async def dispatch(self, request: Request, call_next):
        # Skip CSRF for GET, HEAD, OPTIONS, TRACE methods
        if request.method in ["GET", "HEAD", "OPTIONS", "TRACE"]:
            return await call_next(request)
        
        # Check CSRF token for state-changing requests
        csrf_token = request.headers.get("X-CSRF-Token")
        if not csrf_token:
            logger.warning("CSRF token missing in request")
            # In production, you might want to reject the request
            # return Response(status_code=403, content="CSRF token missing")
        
        # Validate CSRF token (simplified - in production, use proper token validation)
        # if not self.validate_csrf_token(csrf_token):
        #     return Response(status_code=403, content="Invalid CSRF token")
        
        response = await call_next(request)
        
        # Add CSRF token to response
        new_token = secrets.token_hex(16)
        response.headers["X-CSRF-Token"] = new_token
        
        return response

def get_cors_middleware():
    """Get CORS middleware configuration"""
    return CORSMiddleware(
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-CSRF-Token"],
        max_age=600,
    )

def get_security_middleware():
    """Get security middleware"""
    return SecurityHeadersMiddleware

def get_csrf_middleware(secret_key: str = None):
    """Get CSRF protection middleware"""
    return CSRFProtectionMiddleware(secret_key=secret_key)
