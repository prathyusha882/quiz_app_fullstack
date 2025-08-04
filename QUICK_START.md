# Quiz App - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the Quiz App running on your local machine quickly.

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## ⚡ Quick Setup

### 1. Clone and Setup Backend

```bash
# Navigate to backend
cd quiz-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start backend server
python manage.py runserver 8000
```

### 2. Setup Frontend

```bash
# Open new terminal and navigate to frontend
cd quiz-frontend

# Install dependencies
npm install

# Start frontend server
npm start
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 🔧 Environment Setup

### Backend Environment (Optional)

Create `quiz-backend/.env`:

```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment (Optional)

Create `quiz-frontend/.env`:

```bash
REACT_APP_API_URL=http://localhost:8000
```

## 🧪 Test the Application

### 1. Register a New User
- Go to http://localhost:3000
- Click "Register"
- Fill in your details
- Verify your email (check console for email)

### 2. Create a Quiz (Admin)
- Login to http://localhost:8000/admin
- Create a new quiz
- Add questions and options
- Publish the quiz

### 3. Take a Quiz
- Login to the frontend
- Browse available quizzes
- Start a quiz and answer questions
- View your results

## 🔍 API Testing

### Test Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "confirm_password": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Test Quiz API

```bash
# Get quizzes (with auth token)
curl -X GET http://localhost:8000/api/quizzes/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🐳 Docker Quick Start

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Containers

```bash
# Backend
cd quiz-backend
docker build -t quiz-backend .
docker run -p 8000:8000 quiz-backend

# Frontend
cd quiz-frontend
docker build -t quiz-frontend .
docker run -p 3000:3000 quiz-frontend
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   
   # Kill process on port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **Database Issues**
   ```bash
   # Reset database
   python manage.py flush
   python manage.py migrate
   ```

3. **Node Modules Issues**
   ```bash
   # Clear node modules
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Python Environment Issues**
   ```bash
   # Recreate virtual environment
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Debug Commands

```bash
# Check Django status
python manage.py check

# Check migrations
python manage.py showmigrations

# Test database connection
python manage.py dbshell

# Check frontend build
npm run build
```

## 📊 Verify Installation

### Backend Health Check

```bash
curl http://localhost:8000/
# Should return: "Welcome to the Quiz App backend!"
```

### Frontend Health Check

```bash
curl http://localhost:3000/
# Should return the React app HTML
```

### API Health Check

```bash
curl http://localhost:8000/api/auth/
# Should return available auth endpoints
```

## 🎯 Next Steps

1. **Explore the Admin Panel**: http://localhost:8000/admin
2. **Create Sample Data**: Add quizzes and questions
3. **Test User Flows**: Register, login, take quizzes
4. **Review Documentation**: Check the detailed guides
5. **Deploy to Production**: Follow the deployment guide

## 📞 Need Help?

1. Check the troubleshooting section above
2. Review the detailed documentation
3. Check the console for error messages
4. Verify all services are running
5. Ensure ports are not blocked

---

**🎉 You're all set! The Quiz App is now running locally.** 