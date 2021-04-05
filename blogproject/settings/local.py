from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '% k ^!^6-(z ^ +l*)i6-qg*el % 5*2-@ % +jx)jktqb!5t+j$5q1!9 &')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'blog.lidangqi.com', 'django-blog']

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': os.environ.get('DJANGO_MYSQLPASS_KEY', 'password'),
        'HOST': os.environ.get('DJANGO_MYSQLIP_KEY', '127.0.0.1'),
        'PORT': '3306',
    }
}

# 搜索设置
HAYSTACK_CONNECTIONS['default']['URL'] = 'http://elasticsearch_local:9200/'
