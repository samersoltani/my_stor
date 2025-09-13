import os
from pathlib import Path
import dj_database_url



BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

DEBUG = True
# os.environ.get('DEBUG', 'False') == 'True'


ALLOWED_HOSTS = [
    'web-production-8f4b7.up.railway.app',
    '127.0.0.1', # برای تست در کامپیوتر خودتان
]
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Security settings for production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = [
        f'https://{RENDER_EXTERNAL_HOSTNAME}',
        'https://*.127.0.0.1'
    ]

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
   
    'core',
    'account',
    'cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'stor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'stor.wsgi.application'


# تنظیمات دیتابیس
# DATABASES = {
#     'default': dj_database_url.config(
#         conn_max_age=600,
#         ssl_require=True,
#         default=os.getenv('DATABASE_URL')
#     )
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================
# آدرس URL برای فایل‌های مدیا (عکس‌هایی که کاربران آپلود می‌کنند)
MEDIA_URL = '/media/'
# مسیر پوشه‌ای که فایل‌های مدیا در کامپیوتر شما در آن ذخیره می‌شوند
MEDIA_ROOT = BASE_DIR / 'media'

# آدرس URL برای فایل‌های استاتیک (CSS, JS, عکس‌های قالب)
STATIC_URL = '/static/'
# لیستی از پوشه‌هایی که جنگو باید برای پیدا کردن فایل‌های استاتیک در آنها جستجو کند
# این مهم‌ترین خط است. ما به جنگو می‌گوییم که یک پوشه به نام 'static' در ریشه پروژه وجود دارد
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# مسیری که دستور collectstatic تمام فایل‌های استاتیک را برای محیط پروداکشن در آن کپی می‌کند
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ==============================================================================
# CUSTOM SETTINGS
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CART_SESSION_ID = 'cart'
AUTH_USER_MODEL = 'account.CustomUser'
LOGOUT_REDIRECT_URL = 'core:home'

# Zarinpal Settings
ZARINPAL_CONFIG = {
    'SANDBOX': os.environ.get('SANDBOX', 'True') == 'True',
    'MERCHANT_ID': os.environ.get('MERCHANT_ID', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'),
    'CALLBACK_URL': os.environ.get('ZARINPAL_CALLBACK', 'https://yourdomain.com/zarinpal/verify/')
}
# Email Settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None

else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# تنظیمات امنیتی برای Production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True



MERCHANT = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' 