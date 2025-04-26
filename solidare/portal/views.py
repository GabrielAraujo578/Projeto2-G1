from datetime import datetime
from .models import Professor, Candidato
from .models import Aluno, Aviso, EventoCalendario
import calendar
import json
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.core.mail import send_mail
from django.utils.dateparse import parse_date
from django.utils.safestring import mark_safe
from datetime import date

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # username continua sendo email

        if user is not None:
            login(request, user)

            # Verifica se é professor
            if Professor.objects.filter(user=user).exists():
                return redirect('pagina_professor')

            # Verifica se é um candidato
            try:
                candidato = Candidato.objects.get(user=user)
                if candidato.aprovado:
                    return redirect('pagina_aluno')
                else:
                    return render(request, 'candidato_em_analise.html', {'candidato': candidato})
            except Candidato.DoesNotExist:
                pass  # segue o fluxo

            return redirect('home')

        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password1 = request.POST["password1"]
        
        # Verifica se as senhas são iguais
        if password1 == request.POST["password2"]:
            # Gerar o username a partir do email (se necessário)
            username = email  # O email será usado como username
            
            # Verifica se o email já está registrado
            if User.objects.filter(username=username).exists():
                return render(request, "cadastro.html", {"erro": "Usuário já existe"})
            else:
                # Cria o usuário com o email como username
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                return redirect("login")
        else:
            return render(request, "cadastro.html", {"erro": "As senhas não coincidem"})
    
    return render(request, "cadastro.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def index_view(request):
    return render(request, "index.html")  


def lista_candidatos(request):
    candidatos = Candidato.objects.all()
    return render(request, "candidatos.html", {"candidatos": candidatos})


def get_bool(value):
    return {'on': True, 'true': True, 'True': True, True: True}.get(value, False)

def get_decimal(value):
    try:
        return Decimal(value) if value else None
    except InvalidOperation:
        return None

def get_int(value):
    try:
        return int(value) if value else None
    except ValueError:
        return None

def cadastro_candidato(request):
    if request.method == "POST":
        # 1. Coleta campos principais obrigatórios
        data_nascimento_str = request.POST.get('data_nascimento')
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nome_completo = request.POST.get('nome_completo', '').strip()
        sexo = request.POST.get('sexo')
        aprovado = None

        # 2. Checagens iniciais
        erros = []
        if password1 != password2:
            erros.append("As senhas não coincidem.")
        if User.objects.filter(email=email).exists():
            erros.append("E-mail já cadastrado.")
        if not nome_completo or not data_nascimento_str or not sexo:
            erros.append("Preencha todos os campos obrigatórios.")

        # 3. Gera idade
        data_nascimento = None
        idade = None
        try:
            if data_nascimento_str:
                data_nascimento = date.fromisoformat(data_nascimento_str)
                hoje = date.today()
                idade = hoje.year - data_nascimento.year - int(
                    (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
                )
        except ValueError:
            erros.append("Data de nascimento inválida.")

        if erros:
            return render(request, "cadastro_candidato.html", {"erros": erros, "dados": request.POST})

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=email, email=email, password=password1)
                candidato = Candidato(
                    user=user,
                    nome_completo=nome_completo,
                    data_nascimento=data_nascimento,
                    idade=idade,
                    sexo=sexo,
                    raca_cor=request.POST.get('raca_cor', '').strip(),
                    cpf=request.POST.get('cpf', '').strip(),
                    telefone=request.POST.get('telefone', '').strip(),
                    whatsapp=get_bool(request.POST.get('whatsapp')),
                    estado_civil=request.POST.get('estado_civil', ''),
                    email=email,
                    endereco_principal=request.POST.get('endereco_principal', ''),
                    numero=request.POST.get('numero', ''),
                    bairro=request.POST.get('bairro', ''),
                    municipio_uf=request.POST.get('municipio_uf', ''),
                    microrregiao=request.POST.get('microrregiao', ''),
                    cep=request.POST.get('cep', ''),
                    ingressara_no_projeto=get_bool(request.POST.get('ingressara_no_projeto')),
                    turno=request.POST.get('turno', ''),
                    apadrinhado=get_bool(request.POST.get('apadrinhado')),
                    escolaridade=request.POST.get('escolaridade', ''),
                    rede_ensino=request.POST.get('rede_ensino', ''),
                    ano_ou_periodo=request.POST.get('ano_ou_periodo', ''),
                    turno_escolar=request.POST.get('turno_escolar', ''),
                    motivo_nao_estuda=request.POST.get('motivo_nao_estuda', ''),
                    pretende_estudar=get_bool(request.POST.get('pretende_estudar')),
                    situacao_profissional=request.POST.get('situacao_profissional', ''),
                    profissao=request.POST.get('profissao', ''),
                    local_trabalho=request.POST.get('local_trabalho', ''),
                    bairro_trabalho=request.POST.get('bairro_trabalho', ''),
                    salario=get_decimal(request.POST.get('salario')),
                    conhece_eca=request.POST.get('conhece_eca', ''),
                    nocao_cidadania=get_bool(request.POST.get('nocao_cidadania')),
                    referencia_familiar=request.POST.get('referencia_familiar', ''),
                    conhece_conselho=request.POST.get('conhece_conselho', ''),
                    conhece_foscar=request.POST.get('conhece_foscar', ''),
                    possui_plano=get_bool(request.POST.get('possui_plano')),
                    nome_plano=request.POST.get('nome_plano', ''),
                    problema_saude=get_bool(request.POST.get('problema_saude')),
                    acompanhamento_medico=get_bool(request.POST.get('acompanhamento_medico')),
                    cirurgia=get_bool(request.POST.get('cirurgia')),
                    problema_atual=request.POST.get('problema_atual', ''),
                    deficiencia_fisica=get_bool(request.POST.get('deficiencia_fisica')),
                    tipo_deficiencia=request.POST.get('tipo_deficiencia', ''),
                    desenvolvimento_mental=request.POST.get('desenvolvimento_mental', ''),
                    onde_procura_saude=request.POST.get('onde_procura_saude', ''),
                    refeicoes_dia=get_int(request.POST.get('refeicoes_dia')),
                    alimentacao=request.POST.get('alimentacao', ''),
                    participa_grupo=request.POST.get('participa_grupo', ''),
                    tipo_casa=request.POST.get('tipo_casa', ''),
                    tipo_moradia=request.POST.get('tipo_moradia', ''),
                    vulnerabilidade=request.POST.get('vulnerabilidade', ''),
                    numero_comodos=get_int(request.POST.get('numero_comodos')),
                    divisorias_crianca_adulto=get_bool(request.POST.get('divisorias_crianca_adulto')),
                    tem_banheiro=get_bool(request.POST.get('tem_banheiro')),
                    banheiro_dentro=get_bool(request.POST.get('banheiro_dentro')),
                    energia_publica=get_bool(request.POST.get('energia_publica')),
                    agua=request.POST.get('agua', ''),
                    destino_lixo=request.POST.get('destino_lixo', ''),
                    destino_esgoto=request.POST.get('destino_esgoto', ''),
                    bens=request.POST.get('bens', ''),
                    origem_bens=request.POST.get('origem_bens', ''),
                    cadastrado_cadunico=get_bool(request.POST.get('cadastrado_cadunico')),
                    bolsa_familia=get_bool(request.POST.get('bolsa_familia')),
                    auxilio_moradia=get_bool(request.POST.get('auxilio_moradia')),
                    recebe_bpc=get_bool(request.POST.get('recebe_bpc')),
                    faixa_renda_familiar=request.POST.get('faixa_renda_familiar', ''),
                    renda_per_capita=get_decimal(request.POST.get('renda_per_capita')),
                    aprovado=aprovado,
                )
                candidato.save()
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect('cadastro_sucesso')

        except Exception as e:
            erros.append(f"Erro ao salvar: {e}")
            return render(request, "cadastro_candidato.html", {"erros": erros, "dados": request.POST})

    return render(request, "cadastro_candidato.html")

def cadastro_sucesso(request):
    return render(request, "cadastro_sucesso.html")

def pagina_aluno(request):
    return render(request, 'aluno.html')

def pagina_professor(request):
    return render(request, 'professor.html')


def alterar_status(request, candidato_id):
    if not Professor.objects.filter(user=request.user).exists():
        return redirect('login')  # ou exibir uma página de erro

    candidato = get_object_or_404(Candidato, id=candidato_id)

    if request.method == 'POST':
        # Se veio 'aprovar', está marcado → True
        aprovado = request.POST.get('status') == 'aprovar'
        candidato.aprovado = aprovado
        candidato.save()

        if aprovado:
            # Cria o Aluno se ainda não existir
            Aluno.objects.get_or_create(candidato=candidato)
        else:
            # Remove o Aluno se já existia e o candidato foi reprovado
            Aluno.objects.filter(candidato=candidato).delete()

    return redirect('lista_candidatos')

def verificar_aprovacao(request, candidato_id):
    candidato = Candidato.objects.get(id=candidato_id)
    
    if candidato.aprovado == aprovado:
        return render(request, 'aluno.html', {'candidato': candidato})
    else:
        return render(request, 'candidato_em_analise.html', {'candidato': candidato})

def sobre_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')

        corpo_mensagem = f"""
        Você recebeu uma nova mensagem pelo site:

        Nome: {nome}
        E-mail: {email}
        Assunto: {assunto}
        Mensagem:
        {mensagem}
        """

        send_mail(
            subject=f"[Contato do site] {assunto}",
            message=corpo_mensagem,
            from_email='solidareg1@gmail.com',
            recipient_list=['solidareg1@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, "Mensagem enviada com sucesso! Entraremos em contato em breve.")
        return redirect('confirmacao_email')

    # Aqui trata o GET — renderiza a página de contato
    return render(request, 'sobre.html')

def confirmacao_email_view(request):
    return render(request, 'confirmacao_email.html')

def is_professor(user):
    return Professor.objects.filter(user=user).exists()    

@login_required
def lista_avisos(request):
    avisos = Aviso.objects.all().order_by('-data_criacao')
    eh_professor = Professor.objects.filter(user=request.user).exists()

    return render(request, 'lista_avisos.html', {
        'avisos': avisos,
        'eh_professor': eh_professor,
    })

@login_required
@user_passes_test(is_professor)
def criar_aviso(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        mensagem = request.POST.get('mensagem')

        if titulo and mensagem:
            Aviso.objects.create(
                titulo=titulo,
                mensagem=mensagem,
                autor=request.user  
            )
            return redirect('lista_avisos')

    return render(request, 'criar_aviso.html')

@login_required
def calendario(request):
    now = datetime.now()
    year = now.year
    month = now.month
    today = now.day

    # Pegue os eventos do mês atual
    eventos = EventoCalendario.objects.filter(data__year=year, data__month=month)

    # Transforma em JSON simples
    eventos_json = [
    {
        'id': evento.id,
        'dia': evento.data.day,
        'mes': evento.data.month,
        'ano': evento.data.year,
        'hora': evento.hora.strftime('%H:%M') if evento.hora else '',
        'titulo': evento.titulo
    } for evento in eventos
]


    context = {
        'eventos_json': mark_safe(json.dumps(eventos_json)),
        'month': month,
        'year': year,
    }
    return render(request, 'calendario.html', context)

@login_required
def adicionar_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.GET.get('data')  
        hora = request.POST.get('hora')

        if titulo and descricao and data:
            EventoCalendario.objects.create(
                titulo=titulo,
                descricao=descricao,
                data=data,
                hora=hora,
                aluno=request.user  
            )
            return redirect('calendario')
    
    return render(request, 'adicionar_evento.html')


@login_required
def detalhe_evento(request, id):
    evento = get_object_or_404(EventoCalendario, id=id)

    if request.method == 'POST':
        evento.delete()
        return redirect('calendario')

    return render(request, 'detalhe_evento.html', {'evento': evento})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EventoCalendario

@login_required
def editar_evento(request, id):
    evento = get_object_or_404(EventoCalendario, id=id)

    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo', '')
        evento.descricao = request.POST.get('descricao', '')
        evento.data_inicio = request.POST.get('data_inicio') or None
        evento.data_fim = request.POST.get('data_fim') or None
        evento.horario_inicio = request.POST.get('horario_inicio') or None
        evento.horario_fim = request.POST.get('horario_fim') or None
        evento.local = request.POST.get('local', '')
        evento.save()
        return redirect('detalhe_evento', id=evento.id)

    return render(request, 'editar_evento.html', {'evento': evento})

