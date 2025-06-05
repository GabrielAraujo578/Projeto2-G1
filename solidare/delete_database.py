import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solidare.settings_test')
django.setup()

from django.conf import settings

# Impede uso acidental do banco de produção
if 'db_test.sqlite3' not in str(settings.DATABASES['default']['NAME']):
    raise RuntimeError(f"CUIDADO! Esse script só pode ser executado com o banco de testes. Banco atual: {settings.DATABASES['default']['NAME']}")

from portal.models import Turma, Evento, Aluno

# Apaga tudo exceto usuários
Turma.objects.all().delete()
Evento.objects.all().delete()
Aluno.objects.all().delete()

print("Dados apagados, usuários mantidos.")
