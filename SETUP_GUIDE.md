# 🚀 **COMPLETE SETUP GUIDE FOR QUIZ APP**

## 📋 **PREREQUISITES**

### **Required Software:**
- **Python 3.8+** (Download from [python.org](https://python.org))
- **Node.js 16+** (Download from [nodejs.org](https://nodejs.org))
- **Git** (Download from [git-scm.com](https://git-scm.com))
- **PostgreSQL** (Download from [postgresql.org](https://postgresql.org))
- **Redis** (Download from [redis.io](https://redis.io))

### **For Windows:**
- Install Python from [python.org](https://python.org)
- Install Node.js from [nodejs.org](https://nodejs.org)
- Install Git from [git-scm.com](https://git-scm.com)
- Install PostgreSQL from [postgresql.org](https://postgresql.org)
- Install Redis from [redis.io](https://redis.io) or use WSL

### **For macOS:**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python node git postgresql redis
```

### **For Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nodejs npm git postgresql postgresql-contrib redis-server
```

## 🛠️ **PROJECT SETUP**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/quiz_app_fullstack.git
cd quiz_app_fullstack
```

### **2. Backend Setup**

#### **Navigate to Backend Directory**
```bash
cd quiz-backend
```

#### **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### **Install Python Dependencies**
```bash
pip install -r requirements.txt
```

#### **Set Up Environment Variables**
```bash
# Copy environment template
cp env.production.complete .env

# Edit .env file with your settings
# Windows
notepad .env

# macOS/Linux
nano .env
```

#### **Configure Database**
```bash
# Start PostgreSQL service
# Windows: Start from Services
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
psql -U postgres
CREATE DATABASE quiz_app_dev;
CREATE USER quiz_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE quiz_app_dev TO quiz_user;
\q
```

#### **Run Database Migrations**
```bash
python manage.py migrate
```

#### **Create Superuser**
```bash
python manage.py createsuperuser
```

#### **Start Backend Server**
```bash
python manage.py runserver
```

### **3. Frontend Setup**

#### **Navigate to Frontend Directory**
```bash
cd ../quiz-frontend
```

#### **Install Node.js Dependencies**
```bash
npm install
```

#### **Start Frontend Development Server**
```bash
npm start
```

## 🔧 **CONFIGURATION**

### **Environment Variables (.env file)**

Create a `.env` file in the `quiz-backend` directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=quiz_project.settings

# Database Configuration
DB_NAME=quiz_app_dev
DB_USER=quiz_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### **Database Configuration**

Update `quiz-backend/quiz_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'quiz_app_dev'),
        'USER': os.getenv('DB_USER', 'quiz_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## 🚀 **RUNNING THE APPLICATION**

### **1. Start Backend**
```bash
cd quiz-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py runserver
```

### **2. Start Frontend**
```bash
cd quiz-frontend
npm start
```

### **3. Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## 📦 **PACKAGE INSTALLATION COMMANDS**

### **Backend Dependencies (requirements.txt)**
```bash
pip install Django==5.2.4
pip install djangorestframework==3.16.0
pip install djangorestframework-simplejwt==5.5.0
pip install django-cors-headers==4.7.0
pip install django-allauth==0.60.1
pip install dj-rest-auth==5.0.2
pip install psycopg2-binary==2.9.9
pip install django-redis==5.4.0
pip install django-storages==1.14.2
pip install boto3==1.34.0
pip install django-ckeditor==6.7.0
pip install django-taggit==5.0.1
pip install django-mptt==0.16.0
pip install django-crispy-forms==2.1
pip install crispy-bootstrap4==2023.1
pip install django-guardian==2.4.0
pip install django-axes==6.3.0
pip install django-ratelimit==4.1.0
pip install django-haystack==3.2.1
pip install stripe==7.8.0
pip install reportlab==4.0.7
pip install PyPDF2==3.0.1
pip install celery==5.3.4
pip install django-celery-beat==2.5.0
pip install prometheus-client==0.19.0
pip install django-health-check==3.17.0
pip install channels==4.0.0
pip install channels-redis==4.1.0
pip install django-debug-toolbar==4.2.0
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install python-dateutil==2.8.2
pip install Pillow==10.1.0
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0
```

### **Frontend Dependencies (package.json)**
```bash
npm install react@18.2.0
npm install react-dom@18.2.0
npm install react-router-dom@6.8.1
npm install axios@1.3.4
npm install @testing-library/react@13.4.0
npm install @testing-library/jest-dom@5.16.5
npm install @testing-library/user-event@14.4.3
npm install web-vitals@3.3.0
```

## 🔍 **TROUBLESHOOTING**

### **Common Issues:**

#### **1. Port Already in Use**
```bash
# Kill process on port 8000 (Backend)
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (Frontend)
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

#### **2. Database Connection Issues**
```bash
# Check PostgreSQL status
# Windows: Check Services
# macOS: brew services list
# Linux: sudo systemctl status postgresql

# Start PostgreSQL
# Windows: Start from Services
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

#### **3. Redis Connection Issues**
```bash
# Check Redis status
# Windows: Check if Redis is running
# macOS: brew services list
# Linux: sudo systemctl status redis-server

# Start Redis
# Windows: Start Redis service
# macOS: brew services start redis
# Linux: sudo systemctl start redis-server
```

#### **4. Node Modules Issues**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### **5. Python Virtual Environment Issues**
```bash
# Deactivate current environment
deactivate

# Delete and recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ✅ **VERIFICATION**

### **Test Backend**
```bash
# Test Django server
curl http://localhost:8000/api/users/

# Test admin panel
# Open http://localhost:8000/admin/ in browser
```

### **Test Frontend**
```bash
# Test React app
# Open http://localhost:3000 in browser
```

### **Test Database**
```bash
# Connect to database
psql -U quiz_user -d quiz_app_dev

# List tables
\dt

# Exit
\q
```

## 🎉 **SUCCESS!**

Your Quiz App is now running successfully!

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

### **Next Steps:**
1. Create a superuser account
2. Add some sample quizzes and courses
3. Test user registration and login
4. Explore all features

**Happy coding!** 🚀 