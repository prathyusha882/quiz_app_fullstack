# Quiz App - Full Stack Project

A comprehensive quiz application built with Django REST Framework backend and React frontend, featuring user authentication, quiz management, progress tracking, AI-powered question generation, and advanced features like email notifications, certificate generation, and analytics.

## 🚀 Features

### 👤 Authentication & Roles
- **User Registration & Login** with JWT tokens
- **Role-based Access Control (RBAC)**: Admins, Students, Instructors
- **Password Reset via Email** with secure tokens
- **Email verification on signup** with async processing
- **Account management** with profile updates

### 🧠 Quiz Management (Admin/Instructor)
- **Create/edit/delete Quizzes** with rich content
- **Add/remove/edit Questions** with multiple types:
  - Multiple choice
  - Checkbox (multiple correct answers)
  - Text input
  - Essay (long answer)
  - File upload
- **Define quiz properties**:
  - Difficulty (easy/medium/hard)
  - Tags (React, Python, etc.)
  - Time limit per quiz
  - Passing score
  - Maximum attempts
- **AI Question Generation** using OpenAI/Gemini/Ollama
- **Question bank with tagging system**

### ⏱ Quiz-Taking (Student)
- **Start quiz only once** (disable re-entry)
- **Countdown timer** with auto-submit on timeout
- **Save answers as user progresses**
- **Prevent cheating**:
  - No backtracking (optional)
  - One tab policy (basic detection)
  - Session tracking
  - Violation logging

### 🧮 Result Calculation
- **Automatic grading logic** for:
  - MCQ (Multiple Choice Questions)
  - Checkbox (partial credit support)
  - Manual grading for subjective answers
- **Display comprehensive results**:
  - Total score and percentage
  - Correct/wrong answers breakdown
  - Time taken analysis
  - Performance analytics

### 📊 Advanced Features (Company-Level Expectations)

#### 📈 Leaderboard & Analytics
- **Global leaderboard** (top scorers per quiz)
- **Quiz-wise analytics**:
  - Average score and time
  - Attempts made
  - Pass rate statistics
- **Student dashboard**:
  - Progress tracking over time
  - Attempt history & results
  - Performance trends

#### 📜 Certificate Generation
- **Auto-generate certificate (PDF)** after quiz completion
- **Include comprehensive details**:
  - User name and quiz title
  - Score and performance metrics
  - Completion date
  - Certificate ID
  - Digital signature/logo

#### 📬 Email Notifications (Async)
- **On quiz completion** with performance summary
- **On certificate generation** with download link
- **Password reset** with secure tokens
- **Email verification** on registration
- **Reminder emails** for incomplete quizzes
- **Uses Celery + Redis** for background tasks

#### 🧾 Question Bank + Tagging
- **Filter questions by tags** or difficulty when creating quizzes
- **Reuse questions across quizzes**
- **Advanced search and filtering**
- **Question analytics and performance metrics**

### 🧰 Tech Features (Engineering Depth)

#### 🔌 RESTful API (Backend)
- **Built with Django REST Framework**
- **JWT Auth for protected routes**
- **API versioning support**
- **Comprehensive error handling**
- **Rate limiting and security**

#### 💾 PostgreSQL Relational Modeling
- **Models for**: User, Quiz, Question, Submission, Result, Certificate
- **Use ForeignKeys, ManyToMany** (tags, etc.)
- **Optimized queries** with select_related and prefetch_related
- **Database migrations** and versioning

#### 🖼 File Uploads
- **Upload image-based questions** or explanations
- **Store on S3 or locally** via Django's FileField
- **Support for multiple file types**
- **Secure file handling**

#### 🐳 Docker + Environment Config
- **Dockerize the full stack**
- **.env files for secrets/config**
- **docker-compose for multi-container setup**:
  - PostgreSQL database
  - Redis for caching/Celery
  - Django backend
  - React frontend
  - Celery workers
  - Nginx reverse proxy

### 🤖 Bonus Features (Standout)
- **Proctoring-lite**: Basic cheating detection with session tracking
- **Admin Statistics Panel** with charts and analytics
- **Question Import** from CSV/Excel (planned)
- **Gamification elements**:
  - Badges based on score
  - XP points system (planned)
- **Real-time notifications** (planned)

## 🛠️ Technology Stack

### Backend
- **Django 5.2.4**: Web framework
- **Django REST Framework**: API framework
- **Django CORS Headers**: CORS support
- **Simple JWT**: JWT authentication
- **Celery**: Async task processing
- **Redis**: Message broker and caching
- **PostgreSQL**: Production database
- **ReportLab**: PDF generation
- **Python-dotenv**: Environment variable management

### Frontend
- **React 18**: Frontend framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Chart.js**: Progress visualization
- **Tailwind CSS**: Styling framework

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy
- **Gunicorn**: WSGI server

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- PostgreSQL (for production)
- Redis (for async tasks)

## 🚀 Installation & Setup

### Option 1: Docker Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd quiz_app_fullstack

# Copy environment file
cp env.example .env

# Edit environment variables
nano .env

# Start all services
docker-compose up -d

# Create admin user
docker-compose exec backend python manage.py shell
# In the shell:
from users.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
exit()

# Create sample data
docker-compose exec backend python create_proper_quiz_content.py
```

### Option 2: Local Development Setup

#### 1. Backend Setup

```bash
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

# Set up environment variables
cp ../env.example .env
# Edit .env file with your settings

# Run migrations
python manage.py migrate

# Create admin user
python create_admin_user.py

# Create test user
python create_test_user.py

# Create sample quiz content
python create_proper_quiz_content.py

# Start Redis (for Celery)
redis-server

# Start Celery worker (in new terminal)
celery -A quiz_project worker --loglevel=info

# Start Celery beat (in new terminal)
celery -A quiz_project beat --loglevel=info

# Start the backend server
python manage.py runserver
```

#### 2. Frontend Setup

```bash
cd quiz-frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## 🔐 Default Users

### Admin User
- **Username**: admin
- **Password**: admin123
- **Access**: Full admin privileges

### Test User
- **Username**: testuser
- **Password**: test123
- **Access**: Regular user privileges

## 📱 Usage

### For Users
1. **Register/Login**: Create an account or log in with existing credentials
2. **Verify Email**: Check your email and click the verification link
3. **Browse Quizzes**: View available quizzes on the dashboard
4. **Take Quizzes**: Start a quiz and answer questions within time limit
5. **View Results**: Check your performance and review answers
6. **Track Progress**: Monitor your learning progress over time
7. **Download Certificates**: Get PDF certificates for passed quizzes

### For Admins
1. **Access Admin Panel**: Login with admin credentials
2. **Manage Quizzes**: Create and edit quiz content
3. **Generate Questions**: Use AI to generate new questions
4. **View Analytics**: Monitor user performance and quiz statistics
5. **Manage Users**: Oversee user accounts and roles
6. **Export Results**: Download comprehensive reports

## 🏗️ Project Structure

```
quiz_app_fullstack/
├── quiz-backend/                 # Django backend
│   ├── quiz_project/            # Django settings
│   ├── quizzes/                 # Quiz app
│   ├── results/                 # Results app
│   ├── users/                   # User management
│   ├── templates/               # Email templates
│   └── manage.py
├── quiz-frontend/               # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   └── contexts/           # React contexts
│   └── package.json
├── docker-compose.yml           # Multi-container setup
├── Dockerfile                   # Backend container
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh
- `POST /api/auth/verify-email/` - Email verification
- `POST /api/auth/reset-password/` - Password reset request
- `POST /api/auth/reset-password-confirm/` - Password reset confirmation

### Quizzes
- `GET /api/quizzes/` - List all quizzes
- `GET /api/quizzes/{id}/` - Get quiz details
- `GET /api/quizzes/{id}/questions/` - Get quiz questions
- `POST /api/quizzes/{id}/start/` - Start quiz attempt
- `POST /api/quizzes/{id}/submit/` - Submit quiz answers

### Results
- `GET /api/results/my/` - Get user results
- `GET /api/results/progress/` - Get user progress
- `GET /api/results/leaderboard/` - Get leaderboard
- `GET /api/results/certificates/` - Get user certificates

### Admin
- `GET /api/admin/quizzes/` - Admin quiz management
- `GET /api/admin/users/` - Admin user management
- `GET /api/admin/analytics/` - Admin analytics
- `POST /api/admin/generate-ai-questions/` - AI question generation

## 🎯 Key Features Implemented

### ✅ Core Functionality
- [x] User authentication and authorization with roles
- [x] Email verification and password reset
- [x] Quiz creation and management with advanced features
- [x] Question and option management with multiple types
- [x] Quiz taking interface with anti-cheating measures
- [x] Results submission and storage with analytics
- [x] Progress tracking and performance analytics
- [x] Admin dashboard with comprehensive tools
- [x] Responsive design with modern UI

### ✅ Advanced Features
- [x] JWT token authentication with refresh
- [x] CORS support for frontend-backend communication
- [x] Progress visualization with charts
- [x] Detailed quiz review system
- [x] AI question generation capability
- [x] Certificate generation (PDF)
- [x] Email notifications (async with Celery)
- [x] Leaderboard and analytics
- [x] Anti-cheating features
- [x] Comprehensive error handling
- [x] Mobile-responsive UI

### ✅ Production Ready
- [x] Environment variable configuration
- [x] Database migrations and PostgreSQL support
- [x] Static file handling and S3 support
- [x] Security best practices
- [x] Docker containerization
- [x] Async task processing
- [x] Comprehensive documentation
- [x] Health checks and monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure Django server is running on port 8000
   - Check CORS settings in Django settings
   - Verify database connection

2. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify user credentials
   - Check email verification status

3. **Quiz Submission Fails**
   - Ensure all questions are answered
   - Check network connectivity
   - Verify API endpoint availability
   - Check time limit constraints

4. **Email Not Working**
   - Check email configuration in .env
   - Verify Celery worker is running
   - Check Redis connection
   - Review email service credentials

5. **Certificate Generation Fails**
   - Check media directory permissions
   - Verify ReportLab installation
   - Check file storage configuration

6. **Docker Issues**
   - Ensure Docker and Docker Compose are installed
   - Check container logs: `docker-compose logs`
   - Rebuild containers: `docker-compose build`
   - Clean up volumes if needed

## 📈 Future Enhancements

- [ ] Real-time multiplayer quizzes
- [ ] Advanced analytics dashboard with charts
- [ ] Question categories and advanced tagging
- [ ] Export results to multiple formats
- [ ] Social sharing features
- [ ] Advanced AI question generation
- [ ] Mobile app development
- [ ] WebSocket support for real-time features
- [ ] Advanced proctoring features
- [ ] Gamification system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created as an internship project demonstrating full-stack development skills with Django and React, featuring production-ready features like async processing, email notifications, certificate generation, and comprehensive analytics.

---

**Note**: This is a comprehensive quiz application suitable for educational purposes, internship projects, and learning full-stack development concepts with modern best practices. 