from django.db import models
from datetime import date

class Candidato(models.Model):
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    idade = models.IntegerField(editable = False)
    sexo = models.CharField(max_length=20)
    raca_cor = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20, blank=True)
    whatsapp = models.BooleanField()
    estado_civil = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    endereco_principal = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    municipio_uf = models.CharField(max_length=100)
    microrregiao = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=20)

    ingressara_no_projeto = models.BooleanField()
    turno = models.CharField(max_length=50, blank=True)
    apadrinhado = models.BooleanField()



    # Escolaridade
    escolaridade = models.CharField(max_length=100, blank=True)
    rede_ensino = models.CharField(max_length=50, blank=True)
    ano_ou_periodo = models.CharField(max_length=20, blank=True)
    turno_escolar = models.CharField(max_length=50, blank=True)
    motivo_nao_estuda = models.TextField(blank=True)
    pretende_estudar = models.BooleanField(null=True)

    # Situação Profissional
    situacao_profissional = models.CharField(max_length=100, blank=True)
    profissao = models.CharField(max_length=100, blank=True)
    local_trabalho = models.CharField(max_length=100, blank=True)
    bairro_trabalho = models.CharField(max_length=100, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Conhecimentos
    conhece_eca = models.CharField(max_length=50, blank=True)
    nocao_cidadania = models.BooleanField(null=True)
    referencia_familiar = models.CharField(max_length=20, blank=True)
    conhece_conselho = models.CharField(max_length=100, blank=True)
    conhece_foscar = models.CharField(max_length=100, blank=True)

    # Saúde
    possui_plano = models.BooleanField(null=True)
    nome_plano = models.CharField(max_length=100, blank=True)
    problema_saude = models.BooleanField(null=True)
    acompanhamento_medico = models.BooleanField(null=True)
    cirurgia = models.BooleanField(null=True)
    problema_atual = models.TextField(blank=True)
    deficiencia_fisica = models.BooleanField(null=True)
    tipo_deficiencia = models.CharField(max_length=100, blank=True)
    desenvolvimento_mental = models.TextField(blank=True)
    onde_procura_saude = models.CharField(max_length=100, blank=True)

    # Alimentação
    refeicoes_dia = models.IntegerField(null=True, blank=True)
    alimentacao = models.TextField(blank=True)

    # Grupos comunitários
    participa_grupo = models.TextField(blank=True)

    # Moradia
    tipo_casa = models.CharField(max_length=100, blank=True)
    tipo_moradia = models.CharField(max_length=100, blank=True)
    vulnerabilidade = models.TextField(blank=True)
    numero_comodos = models.IntegerField(null=True, blank=True)
    divisorias_crianca_adulto = models.BooleanField(null=True)
    tem_banheiro = models.BooleanField(null=True)
    banheiro_dentro = models.BooleanField(null=True)
    energia_publica = models.BooleanField(null=True)
    agua = models.CharField(max_length=100, blank=True)
    destino_lixo = models.CharField(max_length=100, blank=True)
    destino_esgoto = models.CharField(max_length=100, blank=True)

    # Bens
    bens = models.TextField(blank=True)
    origem_bens = models.CharField(max_length=100, blank=True)

    # Política de Assistência
    cadastrado_cadunico = models.BooleanField(null=True)
    bolsa_familia = models.BooleanField(null=True)
    auxilio_moradia = models.BooleanField(null=True)
    recebe_bpc = models.BooleanField(null=True)

    # Renda
    faixa_renda_familiar = models.CharField(max_length=100, blank=True)
    renda_per_capita = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def save(self, *args, **kwargs):
        hoje = date.today()
        self.idade = hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo


class Responsavel(models.Model):
    responsavel_nome = models.CharField(max_length=200, blank=True)
    responsavel_data_nascimento = models.DateField(null=True, blank=True)
    responsavel_idade = models.IntegerField(null=True, blank=True)
    responsavel_sexo = models.CharField(max_length=20, blank=True)
    responsavel_raca_cor = models.CharField(max_length=50, blank=True)
    responsavel_cpf = models.CharField(max_length=14, blank=True)
    responsavel_telefone = models.CharField(max_length=20, blank=True)
    responsavel_whatsapp = models.BooleanField(default=False)
    responsavel_estado_civil = models.CharField(max_length=50, blank=True)
    responsavel_email = models.EmailField(blank=True)

class Aluno(models.Model):
    Candidato = models.OneToOneField('Candidato', on_delete=models.CASCADE)
    turma = models.ForeignKey('Turma', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Aluno: {self.beneficiario.nome_completo}'

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Prof. {self.nome}'
