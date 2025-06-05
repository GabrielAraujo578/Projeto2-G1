from .settings import *
from pathlib import Path


# Ativa debug temporariamente para facilitar depuração via navegador
DEBUG = True


# Banco de dados separado para testes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}


# Usa um hasher mais rápido para acelerar testes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]


# Backend de e-mail em memória para não enviar e-mails reais
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


# Caminho para os arquivos estáticos durante o desenvolvimento/teste
STATIC_URL = '/static/'


STATICFILES_DIRS = [
    BASE_DIR / 'solidare' / 'portal' / 'static',
]


# Aqui adiciona essa linha para usar o arquivo de URLs específico para teste
ROOT_URLCONF = 'solidare.urls'
