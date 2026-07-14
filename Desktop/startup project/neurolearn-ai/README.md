# NeuroLearn AI

An AI-powered personalized learning platform that adapts to each student's unique learning style, pace, and needs using advanced machine learning and digital twin technology.

## ?? Features

### Core AI Features
- **AI-Powered Chat**: Intelligent tutoring system with RAG (Retrieval-Augmented Generation)
- **Vision AI**: OCR and document analysis for handwritten notes, textbooks, and study materials
- **Multi-Agent System**: Specialized AI agents for coding, research, career guidance, and analytics
- **Student Digital Twin**: Personalized learning profile that adapts to individual learning patterns
- **AI Predictions**: Exam score predictions and learning analytics using LSTM models
- **Smart Recommendations**: Personalized study plans and revision schedules

### Learning Management
- **Document Upload**: Support for PDFs, images, and handwritten notes
- **Quiz Generation**: AI-generated quizzes from uploaded content
- **Study Planner**: Create and manage personalized study schedules
- **Revision Planner**: Spaced repetition for optimal retention
- **Progress Tracking**: Comprehensive learning analytics and performance metrics

### User Roles
- **Students**: Access AI features, upload content, track progress
- **Teachers**: Create courses, manage assignments, track student progress
- **Parents**: Monitor child's learning progress, receive notifications
- **Admins**: System management, user administration, analytics

### Enterprise Features
- **Subscription Management**: Stripe integration for payment processing
- **Rate Limiting**: API rate limiting with Redis support
- **Security**: JWT authentication, RBAC, audit logging, security headers
- **Caching**: Redis caching for improved performance
- **WebSocket**: Real-time notifications and live chat
- **Audit Logging**: Comprehensive system event tracking

## ??? Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Cache**: Redis
- **Authentication**: Firebase Auth + JWT
- **AI/ML**: 
  - LangChain for RAG
  - OpenAI/Ollama for LLMs
  - TensorFlow/Keras for predictions
  - PyTorch for computer vision
  - PaddleOCR for OCR
- **Task Queue**: Celery
- **Payment**: Stripe

### Frontend
- **Framework**: Next.js 14 (React)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Icons**: Lucide React

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Deployment**: Vercel (frontend), Render/Railway (backend)

## ?? Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB
- Redis
- Firebase project (for authentication)
- Stripe account (for payments)
- OpenAI API key or Ollama (for AI features)

## ?? Installation

### Backend Setup

1. Clone the repository:
`ash
git clone https://github.com/yourusername/neurolearn-ai.git
cd neurolearn-ai/backend
`

2. Create a virtual environment:
`ash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
`

3. Install dependencies:
`ash
pip install -r requirements.txt
`

4. Configure environment variables:
`ash
cp .env.example .env
`

Edit .env with your configuration:
`env
# Application
APP_NAME=NeuroLearn AI
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=neurolearn

# Redis
REDIS_URL=redis://localhost:6379

# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=http://localhost:3000

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Stripe
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-webhook-secret
STRIPE_PUBLISHABLE_KEY=your-publishable-key
`

5. Start the backend server:
`ash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

### Frontend Setup

1. Navigate to the frontend directory:
`ash
cd frontend
`

2. Install dependencies:
`ash
npm install
`

3. Configure environment variables:
`ash
cp .env.example .env.local
`

Edit .env.local:
`env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
`

4. Start the development server:
`ash
npm run dev
`

## ?? Docker Setup

Using Docker Compose for local development:

`ash
docker-compose up -d
`

This will start:
- MongoDB (port 27017)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)

## ?? API Documentation

Once the backend is running, access the API documentation at:
`
http://localhost:8000/docs
`

## ?? Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control (RBAC)**: Granular permissions for different user roles
- **Rate Limiting**: API rate limiting to prevent abuse
- **Security Headers**: CSP, HSTS, X-Frame-Options, etc.
- **CSRF Protection**: Cross-site request forgery protection
- **Audit Logging**: Comprehensive logging of system events
- **Input Validation**: Pydantic models for request validation

## ?? Testing

Run backend tests:
`ash
pytest backend/tests/
`

Run frontend tests:
`ash
npm test
`

## ?? Architecture

The application follows a microservices-inspired architecture:

`
+-------------+    +-------------+    +-------------+
¦   Frontend  ¦    ¦   Backend   ¦    ¦   Database  ¦
¦  (Next.js)  ¦?--?¦  (FastAPI)  ¦?--?¦  (MongoDB)  ¦
+-------------+    +-------------+    +-------------+
                          ¦
                          ?
                    +-------------+
                    ¦    Redis    ¦
                    ¦   (Cache)   ¦
                    +-------------+
`

## ?? Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## ?? License

This project is licensed under the MIT License.

## ?? Team

- Your Name - Lead Developer
- Team Members

## ?? Acknowledgments

- LangChain for the RAG framework
- OpenAI for GPT models
- Firebase for authentication
- Stripe for payment processing
- The open-source community

## ?? Support

For support, email support@neurolearn.ai or open an issue on GitHub.

## ??? Roadmap

- [ ] Mobile app development (React Native)
- [ ] Advanced analytics dashboard
- [ ] Integration with more LLM providers
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Video lecture analysis
- [ ] Collaborative study groups
- [ ] Gamification features

---

**Built with ?? for the future of education**
