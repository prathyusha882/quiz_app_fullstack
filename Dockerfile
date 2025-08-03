# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=quiz_project.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        libpng-dev \
        libgif-dev \
        libwebp-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        libxcb1-dev \
        pkg-config \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY quiz-backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY quiz-backend/ /app/

# Create media and static directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "quiz_project.wsgi:application"] 