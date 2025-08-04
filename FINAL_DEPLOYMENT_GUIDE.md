# Quiz App - Final Deployment Guide

## 🚀 Complete Deployment Instructions

This guide provides step-by-step instructions to deploy the Quiz App to production.

### 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (for production)
- Redis (for production)
- Docker & Docker Compose (optional)

### 🏗️ Project Structure

```
quiz_app_fullstack/
├── quiz-backend/          # Django REST API
│   ├── quiz_project/      # Django settings
│   ├── users/            # User management
│   ├── quizzes/          # Quiz functionality
│   ├── results/          # Results tracking
│   ├── courses/          # Course management
│   ├── analytics/        # Analytics
│   ├── payments/         # Payment processing
│   └── proctoring/       # Proctoring features
├── quiz-frontend/         # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── contexts/     # React contexts
└── docker-compose.yml    # Docker configuration
```

### 🔧 Backend Setup

#### 1. Environment Configuration

Create `.env` file in `quiz-backend/`:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secure-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/quiz_app

# Redis
REDIS_URL=redis://localhost:6379

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com

# Frontend URL
FRONTEND_URL=https://your-domain.com

# JWT
JWT_SIGNING_KEY=your-jwt-signing-key

# AI Services (optional)
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-key

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

#### 2. Install Dependencies

```bash
cd quiz-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Static Files

```bash
python manage.py collectstatic
```

#### 5. Start Backend Server

```bash
# Development
python manage.py runserver 8000

# Production (with Gunicorn)
gunicorn quiz_project.wsgi:application --bind 0.0.0.0:8000
```

### 🎨 Frontend Setup

#### 1. Environment Configuration

Create `.env` file in `quiz-frontend/`:

```bash
REACT_APP_API_URL=https://api.your-domain.com
```

#### 2. Install Dependencies

```bash
cd quiz-frontend
npm install
```

#### 3. Build for Production

```bash
npm run build
```

#### 4. Start Frontend Server

```bash
# Development
npm start

# Production (serve build folder)
npx serve -s build -l 3000
```

### 🐳 Docker Deployment

#### 1. Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 2. Individual Docker Containers

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

### 🌐 Production Deployment

#### 1. Nginx Configuration

Create `/etc/nginx/sites-available/quiz-app`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Frontend
    location / {
        root /var/www/quiz-frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/quiz-backend/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /var/www/quiz-backend/media/;
    }
}
```

#### 2. Systemd Services

Create `/etc/systemd/system/quiz-backend.service`:

```ini
[Unit]
Description=Quiz App Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/quiz-backend
Environment=PATH=/var/www/quiz-backend/venv/bin
ExecStart=/var/www/quiz-backend/venv/bin/gunicorn quiz_project.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3. Start Services

```bash
sudo systemctl enable quiz-backend
sudo systemctl start quiz-backend
sudo systemctl restart nginx
```

### 🔒 Security Checklist

- [ ] Change default Django secret key
- [ ] Set DEBUG=False in production
- [ ] Configure HTTPS with SSL certificate
- [ ] Set up proper CORS settings
- [ ] Configure database with strong passwords
- [ ] Set up proper file permissions
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Regular security updates

### 📊 Monitoring

#### 1. Application Monitoring

- Set up Sentry for error tracking
- Configure logging to external service
- Set up health checks

#### 2. Server Monitoring

- CPU and memory usage
- Disk space monitoring
- Network traffic monitoring
- Database performance monitoring

### 🔄 CI/CD Pipeline

#### GitHub Actions Example

```yaml
name: Deploy Quiz App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.4
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          script: |
            cd /var/www/quiz-app
            git pull origin main
            docker-compose up -d --build
```

### 🚨 Troubleshooting

#### Common Issues

1. **CORS Errors**: Check CORS_ALLOWED_ORIGINS in Django settings
2. **Database Connection**: Verify DATABASE_URL and database permissions
3. **Static Files**: Ensure collectstatic was run and nginx serves static files
4. **JWT Issues**: Check JWT_SIGNING_KEY and token expiration settings
5. **Email Issues**: Verify SMTP settings and credentials

#### Debug Commands

```bash
# Check Django logs
tail -f /var/log/django.log

# Check nginx logs
tail -f /var/log/nginx/error.log

# Check systemd service status
systemctl status quiz-backend

# Test database connection
python manage.py dbshell

# Check Redis connection
redis-cli ping
```

### 📈 Performance Optimization

1. **Database**: Use connection pooling and query optimization
2. **Caching**: Implement Redis caching for frequently accessed data
3. **CDN**: Use CDN for static assets
4. **Compression**: Enable gzip compression in nginx
5. **Image Optimization**: Compress and optimize images

### 🔧 Maintenance

#### Regular Tasks

- Database backups
- Log rotation
- Security updates
- Performance monitoring
- User data cleanup

#### Backup Script

```bash
#!/bin/bash
# Backup database
pg_dump quiz_app > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup media files
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/

# Clean old backups (keep last 7 days)
find . -name "backup_*.sql" -mtime +7 -delete
find . -name "media_backup_*.tar.gz" -mtime +7 -delete
```

### 🎯 Final Checklist

- [ ] All environment variables configured
- [ ] Database migrated and seeded
- [ ] Static files collected
- [ ] SSL certificate installed
- [ ] Nginx configured and tested
- [ ] Systemd services enabled
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Security measures in place
- [ ] Performance optimized
- [ ] Documentation updated

### 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Check system resources
4. Verify configuration files
5. Test individual components

---

**🎉 Congratulations! Your Quiz App is now deployed and ready for production use.** 