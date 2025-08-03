# 🚀 **QUICK SETUP GUIDE**

## 📋 **PREREQUISITES**
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis

## 🛠️ **SETUP STEPS**

### **1. Backend Setup**
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

### **2. Frontend Setup**
```bash
cd quiz-frontend
npm install
npm start
```

### **3. Access URLs**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin/

## ✅ **DONE!**
Your Quiz App is now running! 🎉 