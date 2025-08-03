#!/bin/bash

# Production Deployment Script for Quiz App
# This script handles the deployment of the Django quiz application to production

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
required_vars=("SECRET_KEY" "DB_NAME" "DB_USER" "DB_PASSWORD" "EMAIL_HOST_USER" "EMAIL_HOST_PASSWORD")
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

# Restart services (if using systemd)
if command -v systemctl &> /dev/null; then
    print_status "Restarting services..."
    sudo systemctl restart redis
    sudo systemctl restart postgresql
    sudo systemctl restart nginx
    sudo systemctl restart gunicorn
else
    print_warning "systemctl not available. Please restart services manually."
fi

# Start Celery worker (if needed)
print_status "Starting Celery worker..."
celery -A quiz_project worker --loglevel=info --detach

# Start Celery beat (if needed)
print_status "Starting Celery beat..."
celery -A quiz_project beat --loglevel=info --detach

print_status "✅ Production deployment completed successfully!"

echo ""
echo "📋 Deployment Summary:"
echo "  - Dependencies installed/upgraded"
echo "  - Database migrations applied"
echo "  - Static files collected"
echo "  - Health checks passed"
echo "  - Services restarted"
echo "  - Celery workers started"
echo ""
echo "🔗 Your application should now be running at:"
echo "  - Backend API: https://yourdomain.com/api/"
echo "  - Admin Panel: https://yourdomain.com/admin/"
echo ""
echo "⚠️  Important reminders:"
echo "  - Change the default admin password"
echo "  - Configure your domain name in settings"
echo "  - Set up SSL certificates"
echo "  - Configure monitoring and logging"
echo "  - Set up automated backups"
echo "" 