from .models import Professor, Candidato
from .models import Aluno, Aviso, EventoCalendario, MensagemChat, HorarioAula, HorarioTurma, DiaSemana
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
from datetime import datetime, date, timedelta
from django.db.models import Q
from .models import MensagemChat
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Turma, Aluno, Professor, ConteudoTurma
import random
import string


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
def turmas_aluno(request):
    try:
        candidato = request.user.candidato
        if not candidato.aprovado:
            messages.error(request, 'Acesso não autorizado.')
            return redirect('pagina_aluno')

        aluno, created = Aluno.objects.get_or_create(candidato=candidato)
        turmas = Turma.objects.filter(alunos=aluno)

        if request.method == 'POST':
            codigo = request.POST.get('codigo')
            try:
                turma = Turma.objects.get(codigo=codigo)

                # Adiciona aluno à turma
                turma.alunos.add(aluno)

                # Cria os horários da turma para o usuário
                for horario_turma in turma.horarios.all():
                    for dia in horario_turma.dias.all():
                        HorarioAula.objects.get_or_create(
                            aluno=request.user,
                            dia_semana=dia.dia,
                            horario=horario_turma.hora_inicio,
                            horario_fim=horario_turma.hora_fim,
                            disciplina=turma.nome,
                            professor=turma.professor.nome if turma.professor else "Professor"
                        )

                messages.success(request, 'Matriculado com sucesso!')
                return redirect('turmas_aluno')

            except Turma.DoesNotExist:
                messages.error(request, 'Código de turma inválido.')

        return render(request, 'turmas_aluno.html', {'turmas': turmas})

    except Exception as e:
        messages.error(request, f'Erro: {str(e)}')
        return redirect('pagina_aluno')

@login_required
@user_passes_test(is_professor)
def turmas_professor(request):
    professor = get_object_or_404(Professor, user=request.user)
    turmas = Turma.objects.filter(professor=professor)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        # Gerar código único
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while Turma.objects.filter(codigo=codigo).exists():
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        turma = Turma.objects.create(
            nome=nome,
            descricao=descricao,
            codigo=codigo,
            professor=professor
        )

        # Processar horários
        dias_semana = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fim = request.POST.getlist('hora_fim[]')

        # Garante que cada conjunto (dia, início, fim) é tratado separadamente
        for dia, inicio, fim in zip(dias_semana, horas_inicio, horas_fim):
            horario = HorarioTurma.objects.create(
                turma=turma,
                hora_inicio=inicio,
                hora_fim=fim
            )

            DiaSemana.objects.create(
                horario_turma=horario,
                dia=int(dia)
            )

        messages.success(request, 'Turma criada com sucesso!')
        return redirect('turmas_professor')

    return render(request, 'turmas_professor.html', {'turmas': turmas})


@login_required
def conteudo_turma(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    is_professor = Professor.objects.filter(user=request.user).exists()
    is_aluno = False
    
    if not is_professor:
        try:
            aluno = Aluno.objects.get(candidato__user=request.user, turma=turma)
            is_aluno = True
        except Aluno.DoesNotExist:
            messages.error(request, 'Você não está matriculado nesta turma')
            return redirect('turmas_aluno')
    
    if request.method == 'POST' and is_professor:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        arquivo = request.FILES.get('arquivo')
        
        ConteudoTurma.objects.create(
            turma=turma,
            titulo=titulo,
            descricao=descricao,
            arquivo=arquivo
        )
        messages.success(request, 'Conteúdo adicionado com sucesso!')
        return redirect('conteudo_turma', turma_id=turma.id)
    
    conteudos = turma.conteudos.all().order_by('-data_criacao')
    return render(request, 'conteudo_turma.html', {
        'turma': turma,
        'conteudos': conteudos,
        'is_professor': is_professor,
        'is_aluno': is_aluno
    })

@login_required
def lista_avisos(request):
    avisos = Aviso.objects.order_by('-data_criacao')
    return render(request, 'lista_avisos.html', {'avisos': avisos})

@login_required
def criar_aviso(request):
    if not hasattr(request.user, 'professor') or not request.user.professor:
        return redirect('lista_avisos')  # Redireciona se não for professor

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        mensagem = request.POST.get('conteudo')  # HTML usa 'conteudo'

        if titulo and mensagem:
            aviso = Aviso(titulo=titulo, mensagem=mensagem, criado_por=request.user)
            aviso.save()
            return redirect('lista_avisos')
        else:
            error = "Preencha todos os campos."
            return render(request, 'criar_aviso.html', {'error': error})

    return render(request, 'criar_aviso.html')

@login_required
def calendario(request):
    now = datetime.now()
    year = now.year
    month = now.month
    today = now.day

    eventos = EventoCalendario.objects.filter(data__year=year, data__month=month)

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

    is_professor = request.user.groups.filter(name="Professor").exists()

    context = {
        'eventos_json': mark_safe(json.dumps(eventos_json)),
        'month': month,
        'year': year,
        'is_professor': is_professor  
    }
    return render(request, 'calendario.html', context)

@login_required
def adicionar_evento(request):
    if not request.user.is_authenticated or not is_professor(request.user):
        return redirect('calendario')
    
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
def editar_evento(request, id):
    if not request.user.is_authenticated or not is_professor(request.user):
        return redirect('calendario')

    evento = get_object_or_404(EventoCalendario, id=id)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        hora = request.POST.get('hora')

        if titulo and data:
            evento.titulo = titulo
            evento.descricao = descricao
            evento.data = data
            if hora:
                evento.hora = hora
            evento.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('calendario')
    
    return render(request, 'editar_evento.html', {'evento': evento})

@login_required
def detalhe_evento(request, id):
    if not request.user.is_authenticated or not is_professor(request.user):
        return redirect('calendario')

    evento = get_object_or_404(EventoCalendario, id=id)

    if request.method == 'POST':
        evento.delete()
        return redirect('calendario')

    return render(request, 'detalhe_evento.html', {'evento': evento})

@login_required
def chat_aluno(request):
    # Obtém o professor (assumindo que só existe um)
    professor = Professor.objects.first()
    if not professor:
        messages.error(request, "Nenhum professor encontrado no sistema.")
        return redirect('pagina_aluno')
    
    # Obtém ou cria o candidato associado ao usuário atual
    candidato = get_object_or_404(Candidato, user=request.user)
    
    if not candidato.aprovado:
        messages.error(request, "Apenas alunos aprovados podem acessar o chat.")
        return redirect('pagina_aluno')
    
    # Obtém as mensagens entre o aluno e o professor
    mensagens = MensagemChat.objects.filter(
        (Q(remetente=request.user) & Q(destinatario=professor.user)) |
        (Q(remetente=professor.user) & Q(destinatario=request.user))
    ).order_by('data_envio')
    
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        if mensagem:
            MensagemChat.objects.create(
                remetente=request.user,
                destinatario=professor.user,
                conteudo=mensagem
            )
            return redirect('chat_aluno')
    
    return render(request, 'chat_aluno.html', {
        'mensagens': mensagens,
        'professor': professor
    })

@login_required
@user_passes_test(is_professor)
def lista_chats(request):
    # Obtém todos os candidatos aprovados que enviaram mensagens
    alunos_com_mensagens = User.objects.filter(
        Q(mensagens_enviadas__destinatario=request.user) |
        Q(mensagens_recebidas__remetente=request.user),
        candidato__aprovado=True
    ).distinct()
    
    return render(request, 'lista_chats.html', {
        'alunos': alunos_com_mensagens
    })

@login_required
@user_passes_test(is_professor)
def chat_professor(request, aluno_id):
    aluno = get_object_or_404(User, id=aluno_id)
    candidato = get_object_or_404(Candidato, user=aluno, aprovado=True)
    
    mensagens = MensagemChat.objects.filter(
        (Q(remetente=request.user) & Q(destinatario=aluno)) |
        (Q(remetente=aluno) & Q(destinatario=request.user))
    ).order_by('data_envio')
    
    # Marca mensagens como lidas
    mensagens.filter(destinatario=request.user, lida=False).update(lida=True)
    
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        if mensagem:
            MensagemChat.objects.create(
                remetente=request.user,
                destinatario=aluno,
                conteudo=mensagem
            )
            return redirect('chat_professor', aluno_id=aluno_id)
    
    return render(request, 'chat_professor.html', {
        'mensagens': mensagens,
        'aluno': candidato
    })

from datetime import timedelta, datetime, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HorarioAula  # ajuste conforme seu app


@login_required
def horario(request):
    if not hasattr(request.user, 'candidato') or not request.user.candidato.aprovado:
        messages.error(request, 'Apenas alunos aprovados podem acessar o horário.')
        return redirect('home')

    # Gera horários de 15 em 15 minutos, das 7h às 23h
    horas = [f"{h:02d}:{m:02d}" for h in range(7, 23) for m in (0, 30)]

    aulas = HorarioAula.objects.filter(aluno=request.user)

    grade = {}
    for aula in aulas:
        if not aula.horario or not aula.horario_fim:
            continue

        atual = datetime.combine(date.today(), aula.horario)
        fim = datetime.combine(date.today(), aula.horario_fim)

        while atual < fim:
            hora_str = atual.strftime('%H:%M')
            chave = f"{aula.dia_semana}-{hora_str}"
            if chave not in grade:
                grade[chave] = []
            grade[chave].append(aula)
            atual += timedelta(minutes=30)

    context = {
        'horas': horas,
        'grade': grade,
        'grade_items': grade.items(),  # usado no template para não precisar de filtro custom
    }
    return render(request, 'horario.html', context)



@login_required
def adicionar_aula(request):
    if request.method == 'POST':
        try:
            dia_semana = int(request.POST.get('dia_semana'))
            horario_str = request.POST.get('horario')
            disciplina = request.POST.get('disciplina')
            professor = request.POST.get('professor')

            # Converte "07:00" para objeto time
            horario = datetime.strptime(horario_str, "%H:%M").time()

            HorarioAula.objects.create(
                aluno=request.user,
                dia_semana=dia_semana,
                horario=horario,
                disciplina=disciplina,
                professor=professor
            )

            messages.success(request, 'Aula adicionada com sucesso!')
            return redirect('horario')

        except Exception as e:
            messages.error(request, f'Erro ao adicionar aula: {str(e)}')
            return redirect('horario')

    return redirect('horario')