# quiz-backend/quiz_project/settings.py
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv # Make sure you've installed 'python-dotenv'

# Load environment variables from .env file
# This should be at the very top to ensure variables are loaded before being accessed
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# It's good practice to get SECRET_KEY from environment variables for production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-@e1c+d7%e+t7)x&%#v_g$x+z8o8+x9t@k=v(d_@2^z!c(4$n8') # Use os.getenv and provide a strong fallback for dev


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True' # Get DEBUG from env, default True

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# Ensure ALLOWED_HOSTS is a list of strings, splitting by comma if from env var


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework', # Django REST Framework
    'rest_framework_simplejwt', # Simple JWT for token authentication
    'rest_framework_simplejwt.token_blacklist', # For blacklisting refresh tokens (logout)
    'corsheaders', # For handling CORS (Cross-Origin Resource Sharing)

    # My apps
    'users', # User management app
    'quizzes', # Quiz and Question management app
    'results', # Results management app
]

MIDDLEWARE = [
    # CORS middleware must be placed very high, preferably before any other middleware
    # that might generate responses (like CommonMiddleware, CsrfViewMiddleware).
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quiz_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS lists directories where Django looks for templates.
        # BASE_DIR / "templates" for general project templates.
        # BASE_DIR / "frontend" / "build" for serving React's index.html in production.
        'DIRS': [
            BASE_DIR / "templates",
            BASE_DIR / "frontend" / "build" # React build directory for serving static index.html
        ],
        'APP_DIRS': True, # Allows Django to look for templates in app-specific 'templates' folders
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quiz_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # For PostgreSQL in production:
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'your_db_name',
    #     'USER': 'your_db_user',
    #     'PASSWORD': 'your_db_password',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata' # Set to your local timezone, e.g., 'UTC', 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles" # Directory where static files are collected in production

# ✅ For production build of React, where your frontend's static assets will be served from
STATICFILES_DIRS = [
    # BASE_DIR / 'frontend' / 'build' / 'static', # Path to React build's static assets
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User' # Tells Django to use our custom User model

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Optional: for browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Default to require authentication
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # Optional: for browsable API
    ],
}

# Simple JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60), # Access token valid for 60 minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),    # Refresh token valid for 1 day
    "ROTATE_REFRESH_TOKENS": True, # ✅ Set to True to rotate refresh tokens on refresh
    "BLACKLIST_AFTER_ROTATION": True, # ✅ Blacklist old refresh token on rotation
    "UPDATE_LAST_LOGIN": True, # Record last login time

    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv('JWT_SIGNING_KEY', SECRET_KEY), # Use a separate JWT key from env, or fallback to SECRET_KEY
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "JTI_TOKEN_TYPE": "jti",
}


# CORS Headers settings
# https://pypi.org/project/django-cors-headers/
# ✅ For development, allow all origins. In production, specify allowed origins for security.
CORS_ALLOW_ALL_ORIGINS = True # <-- THIS IS KEY FOR LOCAL DEVELOPMENT

# If CORS_ALLOW_ALL_ORIGINS is False, then use CORS_ALLOWED_ORIGINS:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000", # Your frontend URL
#     "http://localhost:3001", # Your frontend URL (alternative port)
#     "http://127.0.0.1:3000",
#     "http://127.0.0.1:3001",
#     "https://yourfrontend.com", # Your production frontend domain
# ]

# ✅ Essential headers for JWT and other common requests
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization', # Important for JWT
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken', # Important for Django's CSRF
    'x-requested-with',
]

# ✅ Essential methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# AI Service API Keys (e.g., for OpenAI or Google Gemini/Ollama)
# You should get these from your .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OLLAMA_API_BASE_URL = os.getenv('OLLAMA_API_BASE_URL', 'http://localhost:11434') # Default Ollama URL

# Ensure at least one is present if needed for startup in DEBUG mode
if DEBUG and not OPENAI_API_KEY and not GOOGLE_API_KEY and not OLLAMA_API_BASE_URL:
    print("WARNING: AI API key/URL not found in environment variables. AI generation might not work.")