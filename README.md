# 🎯 Enterprise Quiz Application

A comprehensive, full-stack quiz platform built with Django and React.

## 🌟 Features

- **Learning Management System** - Courses, lessons, progress tracking
- **Advanced Quiz System** - 10+ question types, auto-scoring
- **Proctoring & Security** - Webcam monitoring, screen recording
- **Payment Processing** - Stripe integration
- **Analytics & Reporting** - Detailed insights and metrics
- **OAuth Authentication** - Google and GitHub login

## 🛠️ Tech Stack

**Backend:** Django 5.2.4, PostgreSQL, Redis, Stripe, AWS S3
**Frontend:** React 18.2.0, React Router DOM, Axios
**DevOps:** Docker, Nginx, Gunicorn, SSL/HTTPS

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/quiz_app_fullstack.git
cd quiz_app_fullstack
```

2. **Backend Setup**
```bash
cd quiz-backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
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

4. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

## 🔒 Security Features

- ✅ JWT Authentication
- ✅ OAuth Integration (Google, GitHub)
- ✅ Email Verification
- ✅ Password Reset
- ✅ Rate Limiting
- ✅ CSRF Protection

## 📖 Documentation

- [Setup Guide](SETUP_GUIDE.md)
- [Production Deployment](COMPLETE_PRODUCTION_DEPLOYMENT.md)
- [Quick Setup](QUICK_SETUP.md)

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 📝 License

MIT License

---

⭐ **Star this repository if you find it helpful!** 