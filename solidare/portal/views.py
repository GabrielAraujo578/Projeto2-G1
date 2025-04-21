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
        form = CandidatoForm(request.POST)
        email = request.POST.get("email")
        password1 = request.POST.get("password1")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Esse email já está em uso.")
            return render(request, "cadastro_candidato.html", {"form": form})

        if form.is_valid():
            try:
                with transaction.atomic():
                    username = email  # usa o email como username
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    candidato = form.save(commit=False)
                    candidato.user = user
                    candidato.save()
                    messages.success(request, "Cadastro realizado com sucesso!")
                    return redirect("cadastro_sucesso")
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {e}")
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")
    else:
        form = CandidatoForm()

    return render(request, "cadastro_candidato.html", {"form": form})

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
        # Aqui você pode adicionar lógica para processar o formulário de contato
        # Por exemplo, enviar um e-mail ou salvar a mensagem no banco de dados
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        
        # Adicione aqui a lógica para processar os dados do formulário
        # Por enquanto, apenas redirecionamos para a mesma página
        messages.success(request, "Mensagem enviada com sucesso! Entraremos em contato em breve.")
        return redirect('sobre')
    
    return render(request, 'sobre.html')

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

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    context = {
        'month_days': month_days,
        'weekdays': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'],
        'today': today,
        'month_name': calendar.month_name[month],
        'year': year,
    }
    return render(request, 'calendario.html', context)

@login_required
# views.py
def adicionar_evento(request):
    data = request.GET.get('data')
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = EventoForm(initial={'data': data})
    return render(request, 'adicionar_evento.html', {'form': form})
