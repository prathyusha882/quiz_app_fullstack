# Quiz App - Full Stack Project

A comprehensive quiz application built with Django REST Framework backend and React frontend, featuring user authentication, quiz management, progress tracking, and AI-powered question generation.

## 🚀 Features

### User Features
- **User Authentication**: Secure login/register system with JWT tokens
- **Quiz Taking**: Interactive quiz interface with multiple-choice questions
- **Progress Tracking**: Visual progress charts and performance analytics
- **Results Review**: Detailed review of quiz attempts with correct answers
- **Responsive Design**: Modern, mobile-friendly UI

### Admin Features
- **Quiz Management**: Create, edit, and delete quizzes
- **Question Management**: Add questions with multiple options
- **AI Question Generation**: Generate questions using AI services
- **Results Analytics**: View all user attempts and performance
- **User Management**: Admin dashboard for user oversight

### Technical Features
- **RESTful API**: Complete backend API with Django REST Framework
- **JWT Authentication**: Secure token-based authentication
- **CORS Support**: Cross-origin resource sharing for frontend-backend communication
- **Database**: SQLite for development, PostgreSQL ready for production
- **Real-time Updates**: Dynamic UI updates without page refresh

## 🛠️ Technology Stack

### Backend
- **Django 5.2.4**: Web framework
- **Django REST Framework**: API framework
- **Django CORS Headers**: CORS support
- **Simple JWT**: JWT authentication
- **Python-dotenv**: Environment variable management

### Frontend
- **React 18**: Frontend framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Chart.js**: Progress visualization
- **Tailwind CSS**: Styling framework

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd quiz_app_fullstack
```

### 2. Backend Setup

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

# Run migrations
python manage.py migrate

# Create admin user
python create_admin_user.py

# Create test user
python create_test_user.py

# Create sample quiz content
python create_proper_quiz_content.py

# Start the backend server
python manage.py runserver
```

### 3. Frontend Setup

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
2. **Browse Quizzes**: View available quizzes on the dashboard
3. **Take Quizzes**: Start a quiz and answer questions
4. **View Results**: Check your performance and review answers
5. **Track Progress**: Monitor your learning progress over time

### For Admins
1. **Access Admin Panel**: Login with admin credentials
2. **Manage Quizzes**: Create and edit quiz content
3. **Generate Questions**: Use AI to generate new questions
4. **View Analytics**: Monitor user performance and quiz statistics

## 🏗️ Project Structure

```
quiz_app_fullstack/
├── quiz-backend/                 # Django backend
│   ├── quiz_project/            # Django settings
│   ├── quizzes/                 # Quiz app
│   ├── results/                 # Results app
│   ├── users/                   # User management
│   └── manage.py
├── quiz-frontend/               # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   └── contexts/           # React contexts
│   └── package.json
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh

### Quizzes
- `GET /api/quizzes/` - List all quizzes
- `GET /api/quizzes/{id}/` - Get quiz details
- `GET /api/quizzes/{id}/questions/` - Get quiz questions

### Results
- `POST /api/results/submit/{quiz_id}/` - Submit quiz answers
- `GET /api/results/my/` - Get user results
- `GET /api/results/progress/` - Get user progress

### Admin
- `GET /api/admin/quizzes/` - Admin quiz management
- `POST /api/admin/generate-ai-questions/` - AI question generation

## 🎯 Key Features Implemented

### ✅ Core Functionality
- [x] User authentication and authorization
- [x] Quiz creation and management
- [x] Question and option management
- [x] Quiz taking interface
- [x] Results submission and storage
- [x] Progress tracking and analytics
- [x] Admin dashboard
- [x] Responsive design

### ✅ Advanced Features
- [x] JWT token authentication
- [x] CORS support for frontend-backend communication
- [x] Progress visualization with charts
- [x] Detailed quiz review system
- [x] AI question generation capability
- [x] Comprehensive error handling
- [x] Mobile-responsive UI

### ✅ Production Ready
- [x] Environment variable configuration
- [x] Database migrations
- [x] Static file handling
- [x] Security best practices
- [x] Comprehensive documentation

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure Django server is running on port 8000
   - Check CORS settings in Django settings

2. **Authentication Issues**
   - Clear browser localStorage
   - Check JWT token expiration
   - Verify user credentials

3. **Quiz Submission Fails**
   - Ensure all questions are answered
   - Check network connectivity
   - Verify API endpoint availability

4. **Progress Not Loading**
   - Check user authentication
   - Verify progress API endpoint
   - Check browser console for errors

## 📈 Future Enhancements

- [ ] Real-time multiplayer quizzes
- [ ] Advanced analytics dashboard
- [ ] Question categories and tags
- [ ] Export results to PDF
- [ ] Email notifications
- [ ] Social sharing features
- [ ] Advanced AI question generation
- [ ] Mobile app development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created as an internship project demonstrating full-stack development skills with Django and React.

---

**Note**: This is a comprehensive quiz application suitable for educational purposes, internship projects, and learning full-stack development concepts. 