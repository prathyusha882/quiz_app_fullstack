#!/bin/bash

# Production Deployment Script for Quiz App
# This script handles the complete deployment process

set -e  # Exit on any error

echo "🚀 Starting production deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "This script must be run from the Django project root directory"
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    print_status "Loading environment variables from .env file"
    export $(cat .env | grep -v '^#' | xargs)
else
    print_warning "No .env file found. Make sure environment variables are set."
fi

# Check required environment variables
required_vars=("SECRET_KEY" "DB_NAME" "DB_USER" "DB_PASSWORD")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        print_error "Required environment variable $var is not set"
        exit 1
    fi
done

print_status "Environment variables validated"

# Install/upgrade dependencies
print_status "Installing/upgrading Python dependencies..."
pip install -r requirements.txt --upgrade

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate --settings=quiz_project.settings_production

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --settings=quiz_project.settings_production

# Create superuser if it doesn't exist
print_status "Checking for superuser..."
python manage.py shell --settings=quiz_project.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
else:
    print("Superuser already exists")
EOF

# Run health checks
print_status "Running health checks..."
python manage.py check --settings=quiz_project.settings_production

# Test database connection
print_status "Testing database connection..."
python manage.py dbshell --settings=quiz_project.settings_production << EOF
SELECT 1;
\q
EOF

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# Set proper permissions
print_status "Setting file permissions..."
chmod 755 logs/
chmod 755 media/
chmod 755 staticfiles/

# Create systemd service files
print_status "Creating systemd service files..."

# Gunicorn service
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=Gunicorn daemon for Quiz App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 quiz_project.wsgi:application --settings=quiz_project.settings_production
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Celery service
sudo tee /etc/systemd/system/celery.service > /dev/null << EOF
[Unit]
Description=Celery Worker Service
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
EnvironmentFile=$(pwd)/.env
WorkingDirectory=$(pwd)
ExecStart=/bin/sh -c '\${WorkingDirectory}/venv/bin/celery multi start w1 -A quiz_project --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log --loglevel=INFO'
ExecStop=/bin/sh -c '\${WorkingDirectory}/venv/bin/celery multi stopwait w1 --pidfile=/var/run/celery/%n.pid'
ExecReload=/bin/sh -c '\${WorkingDirectory}/venv/bin/celery multi restart w1 -A quiz_project --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log --loglevel=INFO'

[Install]
WantedBy=multi-user.target
EOF

# Celery Beat service
sudo tee /etc/systemd/system/celerybeat.service > /dev/null << EOF
[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
EnvironmentFile=$(pwd)/.env
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/celery -A quiz_project beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create log directories
print_status "Creating log directories..."
sudo mkdir -p /var/log/celery
sudo mkdir -p /var/run/celery
sudo chown www-data:www-data /var/log/celery
sudo chown www-data:www-data /var/run/celery

# Reload systemd and start services
print_status "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl enable celery
sudo systemctl start celery
sudo systemctl enable celerybeat
sudo systemctl start celerybeat

# Check service status
print_status "Checking service status..."
sudo systemctl status gunicorn --no-pager -l
sudo systemctl status celery --no-pager -l
sudo systemctl status celerybeat --no-pager -l

print_status "✅ Production deployment completed successfully!"

echo ""
echo "📋 Deployment Summary:"
echo "  - Dependencies installed/upgraded"
echo "  - Database migrations applied"
echo "  - Static files collected"
echo "  - Health checks passed"
echo "  - Services started and enabled"
echo "  - Systemd services configured"
echo ""
echo "🔗 Your application should now be running at:"
echo "  - Backend API: http://localhost:8000/api/"
echo "  - Admin Panel: http://localhost:8000/admin/"
echo ""
echo "⚠️  Important reminders:"
echo "  - Change the default admin password"
echo "  - Configure your domain name in settings"
echo "  - Set up SSL certificates"
echo "  - Configure monitoring and logging"
echo "  - Set up automated backups"
echo ""
echo "📊 Service Status:"
echo "  - Gunicorn: $(sudo systemctl is-active gunicorn)"
echo "  - Celery: $(sudo systemctl is-active celery)"
echo "  - Celery Beat: $(sudo systemctl is-active celerybeat)"
echo "" 