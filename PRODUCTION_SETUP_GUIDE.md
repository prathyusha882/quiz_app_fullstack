# 🚀 Production Setup Guide for Quiz App

This guide will walk you through setting up your enterprise-level quiz application for production deployment.

## 📋 Prerequisites

Before starting, ensure you have:
- A domain name
- A VPS or cloud server (AWS, DigitalOcean, Heroku, etc.)
- PostgreSQL database
- Redis server
- SSL certificate

## 🔧 Step 1: Server Setup

### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Install Required Software
```bash
# Install Python, PostgreSQL, Redis, Nginx
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx git -y

# Install Node.js for frontend (if needed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 1.3 Configure PostgreSQL
```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE quiz_app_prod;
CREATE USER quiz_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE quiz_app_prod TO quiz_user;
\q
```

### 1.4 Configure Redis
```bash
# Redis should be running by default
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## 🔐 Step 2: OAuth Configuration

### 2.1 Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Set Application Type to "Web application"
6. Add authorized redirect URIs:
   - `https://yourdomain.com/accounts/google/login/callback/`
   - `https://yourdomain.com/api/social/google/login/`
7. Copy Client ID and Client Secret

### 2.2 GitHub OAuth Setup
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the details:
   - Application name: "Quiz App"
   - Homepage URL: `https://yourdomain.com`
   - Authorization callback URL: `https://yourdomain.com/accounts/github/login/callback/`
4. Copy Client ID and Client Secret

## 💳 Step 3: Payment Processing Setup

### 3.1 Stripe Configuration
1. Create a [Stripe account](https://stripe.com)
2. Get your API keys from the Dashboard
3. Set up webhook endpoint:
   - URL: `https://yourdomain.com/api/payments/webhook/stripe/`
   - Events to send: `payment_intent.succeeded`, `payment_intent.payment_failed`

### 3.2 PayPal Configuration (Optional)
1. Create a [PayPal Developer account](https://developer.paypal.com)
2. Get your Client ID and Secret
3. Set up webhook endpoint:
   - URL: `https://yourdomain.com/api/payments/webhook/paypal/`

## ☁️ Step 4: AWS S3 Setup (Optional)

### 4.1 Create S3 Bucket
1. Go to [AWS S3 Console](https://console.aws.amazon.com/s3/)
2. Create a new bucket with your domain name
3. Configure bucket for static website hosting
4. Set up CORS configuration:
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
        "AllowedOrigins": ["https://yourdomain.com"],
        "ExposeHeaders": []
    }
]
```

### 4.2 Create IAM User
1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Create a new user with programmatic access
3. Attach the `AmazonS3FullAccess` policy
4. Copy Access Key ID and Secret Access Key

## 📧 Step 5: Email Configuration

### 5.1 Gmail SMTP (Recommended for testing)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use these settings:
   - SMTP Server: smtp.gmail.com
   - Port: 587
   - Security: TLS
   - Username: your-email@gmail.com
   - Password: your-app-password

### 5.2 SendGrid (Recommended for production)
1. Create a [SendGrid account](https://sendgrid.com)
2. Verify your domain
3. Create an API key
4. Use these settings:
   - SMTP Server: smtp.sendgrid.net
   - Port: 587
   - Security: TLS
   - Username: apikey
   - Password: your-sendgrid-api-key

## 🔍 Step 6: Monitoring Setup

### 6.1 Sentry Setup
1. Create a [Sentry account](https://sentry.io)
2. Create a new Django project
3. Copy the DSN (Data Source Name)

### 6.2 Health Checks
The application includes built-in health checks at:
- `https://yourdomain.com/health/`

## 🚀 Step 7: Deployment

### 7.1 Clone Repository
```bash
cd /var/www/
sudo git clone https://github.com/yourusername/quiz_app_fullstack.git
sudo chown -R $USER:$USER quiz_app_fullstack
cd quiz_app_fullstack/quiz-backend
```

### 7.2 Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 7.3 Configure Environment Variables
```bash
cp env.production .env
nano .env
```

Fill in all the required environment variables:
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DJANGO_SETTINGS_MODULE=quiz_project.settings_production

# Database Configuration
DB_NAME=quiz_app_prod
DB_USER=quiz_user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=whsec_your-stripe-webhook-secret

# OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Domain Configuration
DOMAIN_NAME=yourdomain.com
FRONTEND_URL=https://yourdomain.com

# Monitoring and Logging
SENTRY_DSN=your-sentry-dsn

# Security
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1

# SSL/HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 7.4 Run Database Migrations
```bash
python manage.py migrate --settings=quiz_project.settings_production
```

### 7.5 Collect Static Files
```bash
python manage.py collectstatic --noinput --settings=quiz_project.settings_production
```

### 7.6 Create Superuser
```bash
python manage.py createsuperuser --settings=quiz_project.settings_production
```

## 🌐 Step 8: Nginx Configuration

### 8.1 Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/quiz-app
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Static Files
    location /static/ {
        alias /var/www/quiz_app_fullstack/quiz-backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media Files
    location /media/ {
        alias /var/www/quiz_app_fullstack/quiz-backend/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Health Check
    location /health/ {
        proxy_pass http://127.0.0.1:8000;
        access_log off;
    }
}
```

### 8.2 Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/quiz-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Step 9: SSL Certificate

### 9.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 9.2 Get SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9.3 Set Up Auto-renewal
```bash
sudo crontab -e
```

Add this line:
```
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🚀 Step 10: Gunicorn Setup

### 10.1 Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add this configuration:
```ini
[Unit]
Description=Gunicorn daemon for Quiz App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/quiz_app_fullstack/quiz-backend
Environment="PATH=/var/www/quiz_app_fullstack/quiz-backend/venv/bin"
ExecStart=/var/www/quiz_app_fullstack/quiz-backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 quiz_project.wsgi:application --settings=quiz_project.settings_production
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 10.2 Start Gunicorn
```bash
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

## 🔄 Step 11: Celery Setup

### 11.1 Create Celery Service
```bash
sudo nano /etc/systemd/system/celery.service
```

Add this configuration:
```ini
[Unit]
Description=Celery Worker Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
EnvironmentFile=/var/www/quiz_app_fullstack/quiz-backend/.env
WorkingDirectory=/var/www/quiz_app_fullstack/quiz-backend
ExecStart=/bin/sh -c '${WorkingDirectory}/venv/bin/celery multi start w1 -A quiz_project --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log --loglevel=INFO'
ExecStop=/bin/sh -c '${WorkingDirectory}/venv/bin/celery multi stopwait w1 --pidfile=/var/run/celery/%n.pid'
ExecReload=/bin/sh -c '${WorkingDirectory}/venv/bin/celery multi restart w1 -A quiz_project --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log --loglevel=INFO'

[Install]
WantedBy=multi-user.target
```

### 11.2 Create Celery Beat Service
```bash
sudo nano /etc/systemd/system/celerybeat.service
```

Add this configuration:
```ini
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
EnvironmentFile=/var/www/quiz_app_fullstack/quiz-backend/.env
WorkingDirectory=/var/www/quiz_app_fullstack/quiz-backend
ExecStart=/var/www/quiz_app_fullstack/quiz-backend/venv/bin/celery -A quiz_project beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
Restart=always

[Install]
WantedBy=multi-user.target
```

### 11.3 Start Celery Services
```bash
sudo mkdir /var/log/celery
sudo mkdir /var/run/celery
sudo chown www-data:www-data /var/log/celery
sudo chown www-data:www-data /var/run/celery

sudo systemctl enable celery
sudo systemctl start celery
sudo systemctl enable celerybeat
sudo systemctl start celerybeat
```

## 🧪 Step 12: Testing

### 12.1 Test Backend API
```bash
# Test health check
curl https://yourdomain.com/health/

# Test API endpoints
curl https://yourdomain.com/api/users/
```

### 12.2 Test OAuth
1. Visit `https://yourdomain.com/admin/`
2. Go to Social Applications
3. Add Google and GitHub applications with your credentials
4. Test login flows

### 12.3 Test Payment Processing
1. Use Stripe test keys
2. Test payment flow in your application
3. Verify webhook endpoints

## 📊 Step 13: Monitoring

### 13.1 Set Up Log Rotation
```bash
sudo nano /etc/logrotate.d/quiz-app
```

Add this configuration:
```
/var/log/quiz-app/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload gunicorn
    endscript
}
```

### 13.2 Set Up Backup Script
```bash
sudo nano /var/www/quiz_app_fullstack/backup.sh
```

Add this script:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/quiz-app"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump quiz_app_prod > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/quiz_app_fullstack/quiz-backend/media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Make it executable:
```bash
sudo chmod +x /var/www/quiz_app_fullstack/backup.sh
```

Add to crontab:
```bash
sudo crontab -e
```

Add this line:
```
0 2 * * * /var/www/quiz_app_fullstack/backup.sh
```

## 🎉 Step 14: Final Checklist

- [ ] Domain points to your server
- [ ] SSL certificate is installed and working
- [ ] Database is running and accessible
- [ ] Redis is running
- [ ] Nginx is configured and running
- [ ] Gunicorn is running
- [ ] Celery workers are running
- [ ] Environment variables are set
- [ ] Static files are collected
- [ ] Database migrations are applied
- [ ] Superuser is created
- [ ] OAuth providers are configured
- [ ] Payment processing is working
- [ ] Email is configured and working
- [ ] Monitoring is set up
- [ ] Backups are configured
- [ ] Log rotation is set up

## 🚨 Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check Gunicorn logs: `sudo journalctl -u gunicorn`
   - Check Django logs: `tail -f /var/www/quiz_app_fullstack/quiz-backend/logs/django.log`

2. **Database Connection Issues**
   - Verify PostgreSQL is running: `sudo systemctl status postgresql`
   - Check database credentials in `.env`

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic --settings=quiz_project.settings_production`
   - Check Nginx configuration

4. **OAuth Not Working**
   - Verify OAuth credentials in Django admin
   - Check callback URLs match your domain

5. **Payment Processing Issues**
   - Verify Stripe keys are correct
   - Check webhook endpoints are accessible

### Useful Commands

```bash
# Check service status
sudo systemctl status nginx gunicorn celery celerybeat postgresql redis

# View logs
sudo journalctl -u gunicorn -f
sudo journalctl -u celery -f
tail -f /var/www/quiz_app_fullstack/quiz-backend/logs/django.log

# Restart services
sudo systemctl restart nginx gunicorn celery celerybeat

# Check disk space
df -h

# Check memory usage
free -h

# Check network connections
netstat -tulpn
```

## 📞 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all services are running
4. Test each component individually
5. Check the troubleshooting section above

Your enterprise-level quiz application is now ready for production! 🎉 