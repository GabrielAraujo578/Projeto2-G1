import subprocess

cmd = [
    "python",
    "manage.py",
    "flush",
    "--noinput",
    "--settings=solidare.settings_test"
]

print("Limpando o banco de dados de testes...")
subprocess.run(cmd, check=True)
print("Banco limpo com sucesso!")
