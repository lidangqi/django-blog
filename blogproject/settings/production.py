from .common import *
import os
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

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

# 阿里云 CDN 存储静态资源文件 & 阿里云存储上传的图片/文件
# STATICFILES_STORAGE = 'django_oss_storage.backends.OssStaticStorage'

# 阿里云 CDN 存储静态资源文件 & 阿里云存储上传的图片/文件
# STATICFILES_STORAGE = 'django_oss_storage.backends.OssStaticStorage'

DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'

# AliCloud access key ID
OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID', '')
# AliCloud access key secret
OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET', '')
# The name of the bucket to store files in
OSS_BUCKET_NAME = 'django-blog2021'

# The URL of AliCloud OSS endpoint
# Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm for OSS Region & Endpoint
OSS_ENDPOINT = 'oss-cn-shenzhen.aliyuncs.com'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://elasticsearch_local:9200/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    }
}
