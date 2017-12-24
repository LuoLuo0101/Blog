import os
import sys
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

conf = configparser.ConfigParser()

conf_path = os.path.join(BASE_DIR, "Blog")

conf.read(os.path.join(conf_path, "config.ini"), encoding="utf-8")

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = 's+sa+8qr*yqptsl#^qzc#kf^!q)h25w+leeaev0wvoqlk38lr8'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',  # 用户模块
    'operation.apps.OperationConfig',  # 操作模块
    'crispy_forms',  # from 表单验证
    'rest_framework',  # Restful框架
    'corsheaders',  # 解决跨域访问问题
]

# 解决跨域访问问题
CORS_ORIGIN_ALLOW_ALL = True

# 设置默认用户 Model
AUTH_USER_MODEL = 'users.UserProfile'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 设置跨域问题的解决
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'Blog.wsgi.application'

mysql_conf = conf["mysql"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': mysql_conf["NAME"],
        'USER': mysql_conf["USER"],
        'PASSWORD': mysql_conf["PASSWORD"],
        'HOST': mysql_conf["HOST"],
        'PORT': mysql_conf["PORT"],
    }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 文档用的是Session验证的
        'rest_framework.authentication.SessionAuthentication',
        # JWT Token
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

# 设置自定义的登录
AUTHENTICATION_BACKENDS = (
    'users.backend.CustomBackend',
)

import datetime

JWT_AUTH = {
    # 配置过期时间，7 天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 配置认证的开头字符串，你也可以写Token，但是注意前端必须也在headers中传递一样的Token，注意加空格
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
