#!/bin/bash

echo "🚀 Starting production deployment..."

# Install dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python manage.py migrate --settings=quiz_project.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=quiz_project.settings_production

# Create superuser
python manage.py shell --settings=quiz_project.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: admin/admin123")
EOF

# Health checks
python manage.py check --settings=quiz_project.settings_production

echo "✅ Deployment completed!" 