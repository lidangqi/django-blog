from .common import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'blog.lidangqi.com', 'django-blog']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': os.environ['DJANGO_MYSQLPASS_KEY'],
        'HOST': os.environ['DJANGO_MYSQLIP_KEY'],
        'PORT': '3306',
    }
}

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://django-blog-elasticsearch:9200/'
