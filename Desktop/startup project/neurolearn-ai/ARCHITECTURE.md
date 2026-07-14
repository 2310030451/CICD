# NeuroLearn AI - Architecture Documentation

This document provides a comprehensive overview of the NeuroLearn AI system architecture.

## Table of Contents
- [System Overview](#system-overview)
- [Architecture Patterns](#architecture-patterns)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Security Architecture](#security-architecture)
- [Scalability Architecture](#scalability-architecture)
- [Technology Stack](#technology-stack)
- [Database Design](#database-design)
- [API Design](#api-design)
- [Frontend Architecture](#frontend-architecture)

## System Overview

NeuroLearn AI is a microservices-inspired AI-powered learning platform with the following key characteristics:

- **Client-Server Architecture**: Frontend (Next.js) and Backend (FastAPI) separation
- **Event-Driven**: WebSocket support for real-time features
- **Data-Centric**: MongoDB for flexible document storage
- **AI-First**: Multiple AI agents and ML models integrated
- **Security-First**: RBAC, JWT, audit logging, rate limiting

`
+-------------------------------------------------------------+
¦                        User Layer                            ¦
¦  +--------------+  +--------------+  +--------------+      ¦
¦  ¦   Student    ¦  ¦   Teacher    ¦  ¦    Parent    ¦      ¦
¦  +--------------+  +--------------+  +--------------+      ¦
+-------------------------------------------------------------+
                            ¦
                            ?
+-------------------------------------------------------------+
¦                    Presentation Layer                         ¦
¦  +------------------------------------------------------+  ¦
¦  ¦              Next.js Frontend (React)                  ¦  ¦
¦  ¦  - Dashboard Pages  - UI Components  - State Management ¦  ¦
¦  +------------------------------------------------------+  ¦
+-------------------------------------------------------------+
                            ¦
                            ?
+-------------------------------------------------------------+
¦                     Application Layer                         ¦
¦  +------------------------------------------------------+  ¦
¦  ¦              FastAPI Backend (Python)                ¦  ¦
¦  ¦  - API Endpoints  - Business Logic  - AI Integration  ¦  ¦
¦  +------------------------------------------------------+  ¦
+-------------------------------------------------------------+
                            ¦
                            ?
+-------------------------------------------------------------+
¦                      Service Layer                           ¦
¦  +----------+ +----------+ +----------+ +----------+      ¦
¦  ¦   AI     ¦ ¦  Auth    ¦ ¦  Cache   ¦ ¦  Audit   ¦      ¦
¦  ¦ Services ¦ ¦ Service  ¦ ¦  Redis   ¦ ¦  Logger  ¦      ¦
¦  +----------+ +----------+ +----------+ +----------+      ¦
+-------------------------------------------------------------+
                            ¦
                            ?
+-------------------------------------------------------------+
¦                      Data Layer                               ¦
¦  +--------------+          +--------------+                ¦
¦  ¦   MongoDB    ¦          ¦    Redis     ¦                ¦
¦  ¦  (Primary)   ¦          ¦   (Cache)    ¦                ¦
¦  +--------------+          +--------------+                ¦
+-------------------------------------------------------------+
`

## Architecture Patterns

### 1. Layered Architecture

The system follows a classic layered architecture:

- **Presentation Layer**: Next.js frontend with React components
- **Application Layer**: FastAPI backend with business logic
- **Service Layer**: AI services, authentication, caching
- **Data Layer**: MongoDB and Redis

### 2. Repository Pattern

Database access is abstracted through repository-like functions in database.py:

`python
async def get_database():
    return db.database
`

### 3. Dependency Injection

FastAPI's dependency injection is used for:

- Authentication (JWT tokens)
- Database connections
- Configuration settings

### 4. Middleware Pattern

Custom middleware for:

- Security headers
- Rate limiting
- CSRF protection
- Audit logging
- CORS

## Component Architecture

### Backend Components

#### API Layer (pp/api/)
- **Endpoints**: RESTful API route handlers
- **Validation**: Pydantic models for request/response
- **Authentication**: JWT bearer token verification

#### AI Layer (pp/ai/, pp/agents/)
- **RAG Pipeline**: Retrieval-Augmented Generation
- **AI Agents**: Specialized agents (coding, research, career, analytics)
- **ML Models**: LSTM for predictions, Vision AI for OCR

#### Core Layer (pp/core/)
- **Authentication**: JWT token management
- **Authorization**: RBAC system
- **Caching**: Redis cache manager
- **Database**: MongoDB connection management
- **Security**: Security headers and CSRF protection
- **Audit**: System event logging
- **Rate Limiting**: API rate limiting

#### Models Layer (pp/models/)
- **Pydantic Models**: Data validation and serialization
- **Base Schemas**: Common model patterns
- **Response Schemas**: API response structures

#### WebSocket Layer (pp/websocket/)
- **Connection Manager**: WebSocket connection handling
- **Real-time Communication**: Live chat, notifications

### Frontend Components

#### Pages (src/app/)
- **Dashboard**: User dashboard with analytics
- **Admin**: Admin management interface
- **Teacher**: Teacher-specific features
- **Parent**: Parent monitoring interface

#### Components (src/components/)
- **UI Components**: shadcn/ui components
- **Custom Components**: Application-specific components

## Data Flow

### Authentication Flow

`
1. User ? Firebase Auth ? ID Token
2. Frontend ? Backend (ID Token)
3. Backend ? Firebase Verification
4. Backend ? JWT Access Token
5. Frontend ? Store JWT
6. Subsequent Requests ? JWT in Header
`

### Document Upload Flow

`
1. User Uploads Document
2. Frontend ? Upload API
3. Backend ? Store in MongoDB
4. Backend ? Extract Text (OCR/Vision AI)
5. Backend ? Store in ChromaDB (RAG)
6. Backend ? Return Document ID
`

### AI Query Flow

`
1. User Submits Query
2. Frontend ? Chat API
3. Backend ? Agent Orchestrator
4. Agent ? RAG Pipeline
5. RAG ? Retrieve Context
6. LLM ? Generate Response
7. Backend ? Stream Response
8. Frontend ? Display Response
`

### Subscription Flow

`
1. User Initiates Subscription
2. Frontend ? Create Checkout Session
3. Backend ? Stripe API
4. Stripe ? Checkout URL
5. User ? Complete Payment
6. Stripe ? Webhook
7. Backend ? Update Subscription
8. Backend ? Notify User
`

## Security Architecture

### Authentication
- **Firebase Auth**: Primary authentication provider
- **JWT Tokens**: Session management
- **Refresh Tokens**: Long-lived session renewal

### Authorization
- **RBAC**: Role-Based Access Control
- **Permissions**: Granular permission system
- **Role Hierarchy**: Admin > Teacher > Parent > Student

### Security Measures
- **Rate Limiting**: API rate limiting per endpoint type
- **CSRF Protection**: Cross-site request forgery prevention
- **Security Headers**: CSP, HSTS, X-Frame-Options
- **Input Validation**: Pydantic model validation
- **Audit Logging**: Comprehensive event tracking

## Scalability Architecture

### Horizontal Scaling
- **Stateless API**: Backend can be scaled horizontally
- **Load Balancing**: Multiple backend instances
- **Database Sharding**: MongoDB sharding capability

### Vertical Scaling
- **Resource Optimization**: Efficient resource usage
- **Caching**: Redis caching reduces database load
- **Connection Pooling**: Database connection management

### Caching Strategy
- **Redis**: In-memory caching for frequently accessed data
- **Cache Invalidation**: Time-based and event-based
- **Cache Keys**: Structured key naming convention

## Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Database**: MongoDB (NoSQL document database)
- **Cache**: Redis (in-memory data store)
- **Authentication**: Firebase Auth + JWT
- **AI/ML**: 
  - LangChain (RAG framework)
  - OpenAI/Ollama (LLMs)
  - TensorFlow/Keras (ML predictions)
  - PyTorch (computer vision)
  - PaddleOCR (OCR)
- **Task Queue**: Celery (background tasks)
- **Payment**: Stripe (payment processing)

### Frontend
- **Framework**: Next.js 14 (React framework)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **State Management**: React hooks

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Deployment**: Vercel (frontend), Render/Railway (backend)
- **Monitoring**: Log-based monitoring
- **CI/CD**: GitHub Actions (planned)

## Database Design

### Collections

#### User Collections
- **users**: User accounts and authentication
- **profiles**: User profile information

#### Content Collections
- **documents**: Uploaded documents
- **conversations**: Chat conversations
- **quizzes**: Generated quizzes
- **vision_images**: Analyzed images

#### Learning Collections
- **learning_events**: Learning activity tracking
- **predictions**: AI predictions
- **digital_twins**: Student digital twins
- **study_plans**: Study schedules
- **revision_plans**: Revision schedules
- **recommendations**: AI recommendations
- **agent_memory**: Agent conversation memory

#### System Collections
- **subscriptions**: User subscriptions
- **invoices**: Payment invoices
- **coupons**: Discount coupons
- **payment_history**: Payment records
- **audit_logs**: System audit logs
- **system_metrics**: System performance metrics
- **system_health**: System health status
- **error_logs**: Error tracking

#### Role-Specific Collections
- **courses**: Teacher courses
- **notes**: Teacher notes
- **assignments**: Teacher assignments
- **student_progress**: Student progress tracking
- **attendance_records**: Attendance data
- **batches**: Student batches
- **parent_child_relations**: Parent-child relationships
- **student_progress_reports**: Progress reports for parents
- **parent_notifications**: Parent notifications
- **revision_calendar**: Revision schedules for parents

### Indexes

Database indexes are created for:
- Unique fields (email, firebase_uid, file_hash)
- Foreign keys (user_id, teacher_id, student_id)
- Compound indexes (user_id + timestamp)
- Query optimization (status, date ranges)

## API Design

### RESTful Principles
- **Resource-Based**: URLs represent resources
- **HTTP Methods**: GET, POST, PUT, DELETE
- **Status Codes**: Proper HTTP status codes
- **Versioning**: API versioning (/api/v1/)

### API Structure
`
/api/v1/
+-- auth/              # Authentication endpoints
+-- documents/         # Document management
+-- chat/              # AI chat
+-- vision/            # Vision AI
+-- agents/            # AI agents
+-- analytics/         # Learning analytics
+-- predictions/       # AI predictions
+-- digital-twin/      # Digital twin
+-- recommendations/   # AI recommendations
+-- study-planner/     # Study planning
+-- revision-planner/  # Revision planning
+-- subscriptions/     # Subscription management
+-- webhooks/          # Webhook handlers
+-- admin/             # Admin endpoints
+-- teacher/           # Teacher endpoints
+-- parent/            # Parent endpoints
`

### Response Format
`json
{
  "data": {},
  "message": "Success",
  "status": "success"
}
`

### Error Handling
`json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "status_code": 400
}
`

## Frontend Architecture

### Component Structure
`
src/
+-- app/
¦   +-- dashboard/      # Dashboard pages
¦   +-- admin/          # Admin pages
¦   +-- teacher/        # Teacher pages
¦   +-- parent/         # Parent pages
¦   +-- page.tsx        # Landing page
+-- components/
¦   +-- ui/             # shadcn/ui components
¦   +-- custom/         # Custom components
+-- lib/
    +-- utils.ts        # Utility functions
`

### State Management
- **Local State**: React hooks (useState, useEffect)
- **Global State**: Context API (if needed)
- **Server State**: Fetch API with caching

### Routing
- **File-Based Routing**: Next.js App Router
- **Dynamic Routes**: [id] pattern
- **Nested Routes**: Layout components

### Performance Optimization
- **Code Splitting**: Dynamic imports
- **Image Optimization**: Next.js Image component
- **Lazy Loading**: React.lazy()
- **Memoization**: React.memo, useMemo, useCallback

---

This architecture provides a solid foundation for the NeuroLearn AI platform, enabling scalability, maintainability, and security while supporting advanced AI features.
