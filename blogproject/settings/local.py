from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%k^!^6-(z^+l*)i6-qg*el%5*2-@%+jx)jktqb!5t+j$5q1!9&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://elasticsearch-local:9200/'
