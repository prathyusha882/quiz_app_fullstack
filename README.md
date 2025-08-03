# 🎯 QuizMaster - Enterprise-Level Quiz Platform

A comprehensive, full-stack quiz application built with Django REST Framework and React, featuring advanced authentication, multiple question types, course management, payment processing, and analytics.

## 🌟 **Enterprise Features Implemented**

### 👥 **User Roles & Authentication**
- ✅ **User Registration & Login** - Complete authentication system
- ✅ **Role-based Access Control** - Admin/Instructor/Student roles
- ✅ **OAuth Integration** - Google and GitHub login
- ✅ **Email Verification** - Secure email verification system
- ✅ **Password Reset** - Forgot password via email
- ✅ **JWT Token Authentication** - Secure token-based auth

### 🧩 **Advanced Quiz & Question Management**
- ✅ **Multiple Question Types**:
  - Multiple Choice (MCQ)
  - Checkbox (Multiple Answers)
  - True/False
  - Fill-in-the-blank
  - Match the following
  - Essay (Long Answer)
  - Code questions with IDE integration
  - Audio/Video questions
  - File upload questions
- ✅ **Question Bank** - Import/export via CSV/Excel
- ✅ **Question Tags** - Difficulty, category, topic tagging
- ✅ **AI-Powered Generation** - OpenAI/Gemini/Ollama integration

### 🧑‍💻 **Advanced Quiz Taking Experience**
- ✅ **Timer System** - Per quiz and per question timers
- ✅ **Navigation** - Question navigation with progress tracking
- ✅ **Answer Saving** - Temporary answer saving
- ✅ **Backtracking Control** - Configurable navigation restrictions
- ✅ **Full-screen Mode** - Secure exam environment
- ✅ **Auto-submit** - Automatic submission on timeout
- ✅ **Code Editor** - Monaco Editor for programming questions

### 📊 **Comprehensive Analytics & Results**
- ✅ **Immediate Scoring** - Real-time score calculation
- ✅ **Answer Review** - Detailed answer explanations
- ✅ **Visual Analytics** - Charts and graphs (Chart.js)
- ✅ **Time Analytics** - Per-question time tracking
- ✅ **Performance Reports** - Detailed user performance
- ✅ **PDF Export** - Downloadable result certificates

### 🏆 **Leaderboard & Competition**
- ✅ **Global Leaderboards** - Overall performance rankings
- ✅ **Quiz-specific Leaderboards** - Per-quiz rankings
- ✅ **Score Filtering** - Date, category, user filters
- ✅ **Ranking System** - Score, time, attempts ranking
- ✅ **Admin Reports** - Comprehensive performance analytics

### 🛡️ **Advanced Security & Anti-cheating**
- ✅ **Randomized Questions** - Question and option shuffling
- ✅ **One-time Links** - Secure quiz access
- ✅ **IP Tracking** - Location-based monitoring
- ✅ **Full-screen Detection** - Tab switch alerts
- ✅ **Attempt Limits** - Configurable retry restrictions
- ✅ **Violation Tracking** - Cheating detection system

### 📁 **Quiz Configuration Options**
- ✅ **Public/Private Quizzes** - Access control
- ✅ **Scheduled Quizzes** - Start/end time management
- ✅ **Pass/Fail Criteria** - Configurable passing scores
- ✅ **Retry Limits** - Time gaps between attempts
- ✅ **Weighted Scoring** - Negative marking support

### 📚 **LMS-Style Course Integration**
- ✅ **Course Management** - Complete course creation system
- ✅ **Lesson Organization** - Tree structure for content
- ✅ **Progress Tracking** - Detailed user progress
- ✅ **Prerequisites** - Unlock quizzes after completing materials
- ✅ **Certification** - Course completion certificates
- ✅ **Video Integration** - YouTube/Vimeo embedding

### 💳 **Payment & Monetization**
- ✅ **Stripe Integration** - Professional payment processing
- ✅ **PayPal Support** - Alternative payment method
- ✅ **Subscription System** - Monthly/yearly/lifetime plans
- ✅ **Invoice Generation** - Professional billing
- ✅ **Coupon System** - Discount codes and promotions
- ✅ **Course Pricing** - Free and paid course options

### 📤 **Advanced Admin Panel**
- ✅ **Dashboard Analytics** - User, quiz, attempt statistics
- ✅ **Quiz Management** - Complete CRUD operations
- ✅ **User Management** - Ban/suspend user capabilities
- ✅ **Data Export** - CSV/Excel export functionality
- ✅ **Email Notifications** - Automated user communications
- ✅ **Manual Grading** - Subjective question evaluation

### 🌐 **Modern Tech Stack**
- ✅ **Responsive Design** - Mobile/tablet optimization
- ✅ **Dark Mode** - Complete theme system
- ✅ **SEO Optimization** - Meta tags and structured data
- ✅ **Performance** - Optimized loading and caching
- ✅ **Accessibility** - Screen reader and keyboard support

## 🚀 **Technology Stack**

### **Backend (Django)**
- **Framework**: Django 5.2.4 + Django REST Framework
- **Authentication**: JWT tokens with refresh
- **Database**: PostgreSQL with Redis caching
- **File Storage**: AWS S3 integration
- **Background Tasks**: Celery with Redis
- **Email**: SMTP with template system
- **AI Integration**: OpenAI, Google Gemini, Ollama
- **Payment**: Stripe and PayPal
- **Analytics**: Advanced reporting system

### **Frontend (React)**
- **Framework**: React 19.1.0 with hooks
- **Routing**: React Router DOM
- **State Management**: Context API
- **UI Components**: Custom component library
- **Code Editor**: Monaco Editor integration
- **Charts**: Chart.js with react-chartjs-2
- **Styling**: CSS3 with responsive design
- **Theme**: Dark/Light mode system

### **DevOps & Deployment**
- **Containerization**: Docker with docker-compose
- **Database**: PostgreSQL 15
- **Caching**: Redis 7
- **Web Server**: Gunicorn
- **Static Files**: Whitenoise
- **Environment**: Environment variable management

## 📦 **Installation & Setup**

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### **Quick Start**

1. **Clone the repository**
```bash
git clone <repository-url>
cd quiz_app_fullstack
```

2. **Backend Setup**
```bash
cd quiz-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

3. **Frontend Setup**
```bash
cd quiz-frontend
npm install
npm start
```

4. **Database Setup**
```bash
# Using Docker
docker-compose up -d
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/quiz_app

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Processing
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret

# AI Services
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-key
OLLAMA_API_BASE_URL=http://localhost:11434

# OAuth Providers
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
GITHUB_OAUTH_CLIENT_ID=your-github-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-github-client-secret
```

## 📊 **Features Overview**

### **For Students**
- Take quizzes with various question types
- View detailed results and explanations
- Track progress across courses
- Earn certificates upon completion
- Participate in leaderboards
- Access course materials and videos

### **For Instructors**
- Create comprehensive quizzes
- Design courses with lessons
- Monitor student progress
- Generate detailed analytics
- Award certificates
- Manage course content

### **For Administrators**
- Complete user management
- Advanced analytics dashboard
- Payment processing oversight
- System configuration
- Security monitoring
- Data export capabilities

## 🔒 **Security Features**

- **JWT Authentication** with refresh tokens
- **Role-based Access Control** (RBAC)
- **CSRF Protection** on all forms
- **SQL Injection Prevention** with ORM
- **XSS Protection** with content sanitization
- **Rate Limiting** on API endpoints
- **Secure File Uploads** with validation
- **Anti-cheating Measures** with session tracking

## 📈 **Performance Optimizations**

- **Database Indexing** for fast queries
- **Redis Caching** for session and data
- **CDN Integration** for static assets
- **Image Optimization** with compression
- **Lazy Loading** for large datasets
- **Code Splitting** in React
- **Service Worker** for offline support

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support**

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

---

**Built with ❤️ for modern education and assessment** 