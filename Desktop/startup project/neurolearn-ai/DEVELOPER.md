# NeuroLearn AI - Developer Guide

This guide provides detailed information for developers working on the NeuroLearn AI platform.

## Table of Contents
- [Project Structure](#project-structure)
- [Backend Development](#backend-development)
- [Frontend Development](#frontend-development)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [Authentication & Authorization](#authentication--authorization)
- [Caching Strategy](#caching-strategy)
- [Testing](#testing)
- [Debugging](#debugging)
- [Code Style](#code-style)

## Project Structure

`
neurolearn-ai/
+-- backend/
¦   +-- app/
¦   ¦   +-- api/
¦   ¦   ¦   +-- v1/
¦   ¦   ¦       +-- endpoints/      # API route handlers
¦   ¦   ¦       +-- api.py          # API router
¦   ¦   +-- agents/                 # AI agent implementations
¦   ¦   +-- ai/                     # AI/ML services
¦   ¦   +-- core/                   # Core utilities
¦   ¦   ¦   +-- auth.py            # JWT & authentication
¦   ¦   ¦   +-- cache.py           # Redis caching
¦   ¦   ¦   +-- database.py        # MongoDB connection
¦   ¦   ¦   +-- rbac.py            # Role-based access control
¦   ¦   ¦   +-- rate_limit.py      # Rate limiting
¦   ¦   ¦   +-- security.py        # Security middleware
¦   ¦   ¦   +-- audit.py           # Audit logging
¦   ¦   +-- learning/               # Learning analytics
¦   ¦   +-- models/                 # Pydantic models
¦   ¦   +-- websocket/              # WebSocket server
¦   ¦   +-- config.py               # Configuration
¦   ¦   +-- main.py                 # FastAPI application
¦   +-- requirements.txt
¦   +-- .env.example
+-- frontend/
¦   +-- src/
¦   ¦   +-- app/
¦   ¦   ¦   +-- dashboard/          # Dashboard pages
¦   ¦   ¦   +-- admin/              # Admin pages
¦   ¦   ¦   +-- teacher/            # Teacher pages
¦   ¦   ¦   +-- parent/             # Parent pages
¦   ¦   ¦   +-- page.tsx            # Landing page
¦   ¦   +-- components/            # React components
¦   ¦   +-- lib/                    # Utilities
¦   +-- package.json
¦   +-- .env.example
+-- docker-compose.yml
+-- README.md
`

## Backend Development

### Setting Up Development Environment

1. **Install Python dependencies**:
`ash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
`

2. **Configure environment variables**:
`ash
cp .env.example .env
# Edit .env with your configuration
`

3. **Run the development server**:
`ash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

### Adding New API Endpoints

1. Create a new file in ackend/app/api/v1/endpoints/:
`python
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/endpoint")
async def get_endpoint(token: str = Depends(security)):
    # Your logic here
    return {"message": "Hello"}
`

2. Register the router in ackend/app/api/v1/api.py:
`python
from app.api.v1.endpoints.your_endpoint import router as your_router

api_router.include_router(your_router, prefix="/your-endpoint", tags=["Your Endpoint"])
`

### Database Models

Use Pydantic models for data validation:

`python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class YourModelBase(BaseModel):
    name: str
    description: Optional[str] = None

class YourModelCreate(YourModelBase):
    pass

class YourModelDB(YourModelBase):
    id: str = Field(default_factory=lambda: str(datetime.utcnow().timestamp()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
`

### Using the Cache

`python
from app.core.cache import cache, user_cache_key

# Get from cache
user_data = await cache.get(user_cache_key(user_id))

# Set in cache
await cache.set(user_cache_key(user_id), user_data, expire=3600)

# Get or set pattern
user_data = await cache.get_or_set(
    user_cache_key(user_id),
    fetch_user_from_db,
    expire=3600
)
`

### Audit Logging

`python
from app.core.audit import AuditLogger

await AuditLogger.log_event(
    user_id=user_id,
    action="create",
    resource="documents",
    details={"document_id": doc_id}
)
`

## Frontend Development

### Setting Up Development Environment

1. **Install Node dependencies**:
`ash
cd frontend
npm install
`

2. **Configure environment variables**:
`ash
cp .env.example .env.local
# Edit .env.local with your configuration
`

3. **Run the development server**:
`ash
npm run dev
`

### Adding New Pages

1. Create a new page in rontend/src/app/your-page/page.tsx:
`	sx
"use client";

import { useState, useEffect } from "react";

export default function YourPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/endpoint);
    const data = await response.json();
    setData(data);
  };

  return (
    <div>
      <h1>Your Page</h1>
      {/* Your content */}
    </div>
  );
}
`

### Using UI Components

The project uses shadcn/ui components:

`	sx
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <Button>Click me</Button>
  </CardContent>
</Card>
`

### API Calls

Use the fetch API with JWT authentication:

`	sx
const response = await fetch(${process.env.NEXT_PUBLIC_API_URL}/api/v1/endpoint, {
  headers: {
    Authorization: Bearer ,
  },
});
`

## API Reference

### Authentication Endpoints

- POST /api/v1/auth/register - Register new user
- POST /api/v1/auth/login - Login user
- POST /api/v1/auth/refresh - Refresh access token

### Document Endpoints

- POST /api/v1/documents/upload - Upload document
- GET /api/v1/documents - List user documents
- DELETE /api/v1/documents/{id} - Delete document

### AI Endpoints

- POST /api/v1/chat/query - Chat with AI
- POST /api/v1/vision/analyze - Analyze image
- POST /api/v1/agents/route - Route to AI agent

### Learning Endpoints

- GET /api/v1/analytics - Get learning analytics
- GET /api/v1/predictions - Get exam predictions
- GET /api/v1/digital-twin - Get digital twin profile

### Subscription Endpoints

- GET /api/v1/subscriptions - Get user subscription
- POST /api/v1/subscriptions/checkout - Create checkout session
- POST /api/v1/subscriptions/cancel - Cancel subscription

## Database Schema

### Collections

- **users**: User accounts
- **profiles**: User profiles
- **documents**: Uploaded documents
- **conversations**: Chat conversations
- **learning_events**: Learning activity events
- **predictions**: AI predictions
- **digital_twins**: Student digital twins
- **subscriptions**: User subscriptions
- **audit_logs**: System audit logs

### Indexes

Database indexes are automatically created on startup. See ackend/app/core/database.py for the complete index configuration.

## Authentication & Authorization

### JWT Authentication

The system uses JWT tokens for authentication:

- **Access Token**: Short-lived (30 minutes)
- **Refresh Token**: Long-lived (7 days)

### Role-Based Access Control (RBAC)

Roles:
- **admin**: Full system access
- **user**: Standard user access
- **teacher**: Teacher-specific features
- **parent**: Parent-specific features
- **student**: Student-specific features

Permissions are defined in ackend/app/core/rbac.py.

## Caching Strategy

### Redis Caching

Frequently accessed data is cached in Redis:

- User profiles (1 hour)
- Digital twin data (30 minutes)
- Recommendations (15 minutes)
- Analytics data (5 minutes)

Cache keys follow the pattern: {entity}:{id}

## Testing

### Backend Tests

`ash
cd backend
pytest tests/
`

### Frontend Tests

`ash
cd frontend
npm test
`

## Debugging

### Backend Debugging

Enable debug mode in .env:
`env
DEBUG=True
`

Use the loguru logger:
`python
from loguru import logger

logger.info("Info message")
logger.error("Error message")
`

### Frontend Debugging

Use React DevTools and browser console for debugging.

## Code Style

### Backend

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

### Frontend

- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components focused and reusable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## Support

For development questions, contact the development team or open an issue on GitHub.
