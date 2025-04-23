from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CandidatoForm  
from .models import Candidato, Professor, Aluno
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Aviso
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Aviso
from .forms import AvisoForm
from .forms import EventoCalendarioForm
from .models import EventoCalendario
from datetime import datetime
import calendar
from django.utils.dateparse import parse_date
from django.utils.safestring import mark_safe
from datetime import datetime
import json
from django.core.mail import send_mail
from decimal import Decimal, InvalidOperation



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


from django.shortcuts import render

def index_view(request):
    return render(request, "index.html")  


def lista_candidatos(request):
    candidatos = Candidato.objects.all()
    return render(request, "candidatos.html", {"candidatos": candidatos})


def cadastro_candidato(request):
    if request.method == "POST":
        # 1. Coleta campos principais obrigatórios
        data_nascimento_str = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nome_completo = request.POST.get('nome_completo')
        sexo = request.POST.get('sexo')
        aprovado = None  # Adapte se quiser lógica automática

        # 2. Checagens iniciais
        erros = []
        if password1 != password2:
            erros.append("As senhas não coincidem.")
        if User.objects.filter(email=email).exists():
            erros.append("E-mail já cadastrado.")
        if not nome_completo or not data_nascimento_str or not sexo:
            erros.append("Preencha todos os campos obrigatórios.")

        # 3. Gera idade
        data_nascimento_str = request.POST.get('data_nascimento')
        data_nascimento = None
        idade = None
        try:
            if data_nascimento_str:
                data_nascimento = date.fromisoformat(data_nascimento_str)
        except Exception:
            data_nascimento = None

        if data_nascimento is not None:
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - int(
                (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
            )

        if erros:
            contexto = {"erros": erros, "dados": request.POST}
            return render(request, "cadastro_candidato.html", contexto)

        try:
            with transaction.atomic():
                # 4. Criação do usuário
                user = User.objects.create_user(username=email, email=email, password=password1)
                # 5. Criação do Candidato (preenchendo TODOS os campos)
                candidato = Candidato(
                    # User
                    user=user,
                    # Dados pessoais
                    nome_completo=nome_completo,
                    data_nascimento=data_nascimento,
                    idade=idade,
                    sexo=sexo,
                    raca_cor=request.POST.get('raca_cor', ''),
                    cpf=request.POST.get('cpf', ''),
                    telefone=request.POST.get('telefone', ''),
                    whatsapp=request.POST.get('whatsapp') == 'on',
                    estado_civil=request.POST.get('estado_civil', ''),
                    email=email,
                    # Endereço
                    endereco_principal=request.POST.get('endereco_principal', ''),
                    numero=request.POST.get('numero', ''),
                    bairro=request.POST.get('bairro', ''),
                    municipio_uf=request.POST.get('municipio_uf', ''),
                    microrregiao=request.POST.get('microrregiao', ''),
                    cep=request.POST.get('cep', ''),
                    # Projeto
                    ingressara_no_projeto=request.POST.get('ingressara_no_projeto') == 'on',
                    turno=request.POST.get('turno', ''),
                    apadrinhado=request.POST.get('apadrinhado') == 'on',
                    # Escolaridade
                    escolaridade=request.POST.get('escolaridade', ''),
                    rede_ensino=request.POST.get('rede_ensino', ''),
                    ano_ou_periodo=request.POST.get('ano_ou_periodo', ''),
                    turno_escolar=request.POST.get('turno_escolar', ''),
                    motivo_nao_estuda=request.POST.get('motivo_nao_estuda', ''),
                    pretende_estudar={'on': True, 'True': True, True: True}.get(request.POST.get('pretende_estudar'), None),
                    # Situação Profissional
                    situacao_profissional=request.POST.get('situacao_profissional', ''),
                    profissao=request.POST.get('profissao', ''),
                    local_trabalho=request.POST.get('local_trabalho', ''),
                    bairro_trabalho=request.POST.get('bairro_trabalho', ''),
                    salario=Decimal(request.POST['salario']) if request.POST.get('salario') else None,
                    # Conhecimentos
                    conhece_eca=request.POST.get('conhece_eca', ''),
                    nocao_cidadania={'on': True, 'True': True, True: True}.get(request.POST.get('nocao_cidadania'), None),
                    referencia_familiar=request.POST.get('referencia_familiar', ''),
                    conhece_conselho=request.POST.get('conhece_conselho', ''),
                    conhece_foscar=request.POST.get('conhece_foscar', ''),
                    # Saúde
                    possui_plano={'on': True, 'True': True, True: True}.get(request.POST.get('possui_plano'), None),
                    nome_plano=request.POST.get('nome_plano', ''),
                    problema_saude={'on': True, 'True': True, True: True}.get(request.POST.get('problema_saude'), None),
                    acompanhamento_medico={'on': True, 'True': True, True: True}.get(request.POST.get('acompanhamento_medico'), None),
                    cirurgia={'on': True, 'True': True, True: True}.get(request.POST.get('cirurgia'), None),
                    problema_atual=request.POST.get('problema_atual', ''),
                    deficiencia_fisica={'on': True, 'True': True, True: True}.get(request.POST.get('deficiencia_fisica'), None),
                    tipo_deficiencia=request.POST.get('tipo_deficiencia', ''),
                    desenvolvimento_mental=request.POST.get('desenvolvimento_mental', ''),
                    onde_procura_saude=request.POST.get('onde_procura_saude', ''),
                    # Alimentação
                    refeicoes_dia=int(request.POST['refeicoes_dia']) if request.POST.get('refeicoes_dia') else None,
                    alimentacao=request.POST.get('alimentacao', ''),
                    # Grupos comunitários
                    participa_grupo=request.POST.get('participa_grupo', ''),
                    # Moradia
                    tipo_casa=request.POST.get('tipo_casa', ''),
                    tipo_moradia=request.POST.get('tipo_moradia', ''),
                    vulnerabilidade=request.POST.get('vulnerabilidade', ''),
                    numero_comodos=int(request.POST['numero_comodos']) if request.POST.get('numero_comodos') else None,
                    divisorias_crianca_adulto={'on': True, 'True': True, True: True}.get(request.POST.get('divisorias_crianca_adulto'), None),
                    tem_banheiro={'on': True, 'True': True, True: True}.get(request.POST.get('tem_banheiro'), None),
                    banheiro_dentro={'on': True, 'True': True, True: True}.get(request.POST.get('banheiro_dentro'), None),
                    energia_publica={'on': True, 'True': True, True: True}.get(request.POST.get('energia_publica'), None),
                    agua=request.POST.get('agua', ''),
                    destino_lixo=request.POST.get('destino_lixo', ''),
                    destino_esgoto=request.POST.get('destino_esgoto', ''),
                    # Bens
                    bens=request.POST.get('bens', ''),
                    origem_bens=request.POST.get('origem_bens', ''),
                    # Política de Assistência
                    cadastrado_cadunico={'on': True, 'True': True, True: True}.get(request.POST.get('cadastrado_cadunico'), None),
                    bolsa_familia={'on': True, 'True': True, True: True}.get(request.POST.get('bolsa_familia'), None),
                    auxilio_moradia={'on': True, 'True': True, True: True}.get(request.POST.get('auxilio_moradia'), None),
                    recebe_bpc={'on': True, 'True': True, True: True}.get(request.POST.get('recebe_bpc'), None),
                    # Renda
                    faixa_renda_familiar=request.POST.get('faixa_renda_familiar', ''),
                    renda_per_capita=Decimal(request.POST['renda_per_capita']) if request.POST.get('renda_per_capita') else None,
                    # Status
                    aprovado=aprovado,
                )
                candidato.save()
                messages.success(request, "Cadastro realizado com sucesso!")
                return redirect('cadastro_sucesso')

        except (InvalidOperation, Exception) as e:
            erros.append(f"Erro ao salvar: {e}")
            contexto = {"erros": erros, "dados": request.POST}
            return render(request, "cadastro_candidato.html", contexto)
    else:
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

from django.shortcuts import render, redirect
from .models import Candidato

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
    if not hasattr(request.user, 'professor'):
        return HttpResponseForbidden("Apenas professores podem criar avisos.")

    # Resto do código para criar aviso
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            aviso = form.save(commit=False)
            aviso.autor = request.user
            aviso.save()
            return redirect('lista_avisos')
    else:
        form = AvisoForm()

    return render(request, 'criar_aviso.html', {'form': form})

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
    data = request.GET.get('data')  

    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST, aluno=request.user)
        if form.is_valid():
            form.save()
            return redirect('calendario')  
    else:
        form = EventoCalendarioForm(initial={'data': data})

    return render(request, 'adicionar_evento.html', {'form': form})

@login_required
def detalhe_evento(request, id):
    evento = get_object_or_404(EventoCalendario, id=id)

    if request.method == 'POST':
        evento.delete()
        return redirect('calendario')

    return render(request, 'detalhe_evento.html', {'evento': evento})

@login_required
def editar_evento(request, id):
    evento = get_object_or_404(EventoCalendario, id=id)

    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST, instance=evento, aluno=request.user)
        if form.is_valid():
            form.save()
            return redirect('detalhe_evento', id=evento.id)
    else:
        form = EventoCalendarioForm(instance=evento)

    return render(request, 'editar_evento.html', {'form': form, 'evento': evento})
