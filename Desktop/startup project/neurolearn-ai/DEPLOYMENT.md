# NeuroLearn AI - Deployment Guide

This guide covers deployment strategies for the NeuroLearn AI platform.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Backend Deployment (Render/Railway)](#backend-deployment-renderrailway)
- [Database Setup](#database-setup)
- [Redis Setup](#redis-setup)
- [Stripe Configuration](#stripe-configuration)
- [Firebase Configuration](#firebase-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying, ensure you have:
- A Vercel account (for frontend)
- A Render or Railway account (for backend)
- A MongoDB Atlas account (for database)
- A Redis Cloud account (for caching)
- A Firebase project (for authentication)
- A Stripe account (for payments)
- Domain name (optional)

## Environment Setup

### Required Environment Variables

**Backend (.env)**:
`env
APP_NAME=NeuroLearn AI
DEBUG=False

# Server
HOST=0.0.0.0
PORT=8000

# Database
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/neurolearn
MONGODB_DATABASE=neurolearn

# Redis
REDIS_URL=redis://username:password@redis-host:port

# Firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email

# JWT
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=https://yourdomain.com

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Stripe
STRIPE_SECRET_KEY=sk_live_your-secret-key
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
`

**Frontend (.env.local)**:
`env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_your-publishable-key
`

## Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI

`ash
npm install -g vercel
`

### Step 2: Deploy to Vercel

`ash
cd frontend
vercel
`

Follow the prompts:
- Link to your Vercel account
- Set project name
- Configure environment variables
- Deploy

### Step 3: Configure Environment Variables

In Vercel dashboard:
1. Go to Project Settings
2. Add all frontend environment variables
3. Redeploy

### Step 4: Custom Domain (Optional)

1. Go to Domain Settings in Vercel
2. Add your custom domain
3. Configure DNS records

## Backend Deployment (Render/Railway)

### Option 1: Deploy to Render

#### Step 1: Create Render Account

Sign up at [render.com](https://render.com)

#### Step 2: Create New Web Service

1. Connect your GitHub repository
2. Select the backend folder
3. Configure build settings:
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port 

#### Step 3: Configure Environment Variables

Add all backend environment variables in Render dashboard.

#### Step 4: Deploy

Render will automatically deploy on push to main branch.

### Option 2: Deploy to Railway

#### Step 1: Create Railway Account

Sign up at [railway.app](https://railway.app)

#### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

#### Step 3: Configure Service

1. Select backend folder
2. Set environment variables
3. Deploy

## Database Setup

### MongoDB Atlas Setup

1. Create MongoDB Atlas account
2. Create a new cluster
3. Create database user
4. Whitelist your deployment IP
5. Get connection string
6. Update MONGODB_URI in environment variables

### Database Indexes

Indexes are automatically created on application startup. Ensure the application has proper permissions to create indexes.

## Redis Setup

### Redis Cloud Setup

1. Create Redis Cloud account
2. Create a new database
3. Get connection string
4. Update REDIS_URL in environment variables

### Alternative: Self-Hosted Redis

`ash
docker run -d -p 6379:6379 redis:alpine
`

## Stripe Configuration

### Step 1: Create Stripe Account

1. Sign up at [stripe.com](https://stripe.com)
2. Complete account verification
3. Get API keys

### Step 2: Configure Products and Prices

1. Create subscription products in Stripe Dashboard
2. Set up pricing tiers
3. Note price IDs for configuration

### Step 3: Configure Webhooks

1. Create webhook endpoint in Stripe
2. Point to: https://your-backend-url.com/api/v1/webhooks/stripe
3. Select events to monitor:
   - checkout.session.completed
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   - invoice.payment_succeeded
   - invoice.payment_failed

### Step 4: Update Environment Variables

Add Stripe keys to backend environment variables.

## Firebase Configuration

### Step 1: Create Firebase Project

1. Go to Firebase Console
2. Create new project
3. Enable Authentication (Email/Password)
4. Get configuration details

### Step 2: Generate Service Account Key

1. Go to Project Settings
2. Service Accounts
3. Generate Private Key
4. Save JSON file securely

### Step 3: Update Environment Variables

Add Firebase configuration to environment variables.

## Monitoring and Logging

### Application Monitoring

Use services like:
- **Sentry**: Error tracking
- **Datadog**: Application monitoring
- **LogRocket**: User session recording

### Log Management

Configure log aggregation:
- **Papertrail**: Log management
- **Loggly**: Cloud log management
- **CloudWatch**: AWS log management

### Health Checks

The application includes a health check endpoint:
`
GET /health
`

Configure monitoring services to ping this endpoint regularly.

## Security Considerations

### Production Security Checklist

- [ ] Set DEBUG=False in production
- [ ] Use strong, randomly generated secrets
- [ ] Enable HTTPS everywhere
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable security headers
- [ ] Regularly update dependencies
- [ ] Implement backup strategy
- [ ] Monitor for security vulnerabilities
- [ ] Use environment-specific API keys

### SSL/TLS Configuration

- Use Let's Encrypt for free SSL certificates
- Configure proper SSL/TLS settings
- Enable HSTS

### Backup Strategy

- **Database**: Daily backups with 30-day retention
- **Redis**: Enable persistence (AOF/RDB)
- **Application logs**: 90-day retention

## Troubleshooting

### Common Issues

**Build Failures**:
- Check dependency versions
- Verify environment variables
- Review build logs

**Database Connection Issues**:
- Verify MongoDB connection string
- Check IP whitelist
- Ensure database user has correct permissions

**Redis Connection Issues**:
- Verify Redis URL
- Check Redis instance status
- Ensure network connectivity

**Stripe Webhook Failures**:
- Verify webhook secret
- Check webhook URL accessibility
- Review Stripe dashboard logs

### Getting Help

- Check application logs
- Review error messages
- Consult documentation
- Open GitHub issue

## Post-Deployment

### Performance Optimization

1. Enable CDN for static assets
2. Configure caching headers
3. Optimize database queries
4. Monitor application performance

### Scaling

- **Horizontal Scaling**: Add more instances
- **Vertical Scaling**: Increase instance size
- **Database Scaling**: Use read replicas
- **Cache Scaling**: Use Redis Cluster

### Maintenance

- Regular dependency updates
- Security patching
- Database maintenance
- Log rotation
- Backup verification

## CI/CD Pipeline

Consider setting up GitHub Actions for automated testing and deployment. See .github/workflows/ for example configurations.

---

For additional support, refer to the [Developer Guide](DEVELOPER.md) or open an issue on GitHub.
