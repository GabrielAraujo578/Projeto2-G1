from .settings import *

# Banco de dados separado para testes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',  # <- banco de testes separado!
    }
}

# Usa um hasher mais rápido para acelerar testes
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Backend de e-mail em memória para não enviar e-mails reais
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Evita logging desnecessário
DEBUG = False
