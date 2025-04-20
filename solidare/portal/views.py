from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CandidatoForm  
from .models import Candidato 
from django.shortcuts import get_object_or_404


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, "cadastro.html", {"erro": "Usuário já existe"})
            else:
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

@user_passes_test(lambda u: u.is_superuser)
def lista_candidatos(request):
    candidatos = Candidato.objects.all()
    return render(request, "candidatos.html", {"candidatos": candidatos})


def cadastro_candidato(request):
    if request.method == "POST":
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("cadastro_sucesso")  
    else:
        form = CandidatoForm()
    return render(request, "cadastro_candidato.html", {"form": form})

def cadastro_sucesso(request):
    return render(request, "cadastro_sucesso.html")

def pagina_aluno(request):
    return render(request, 'aluno.html')

def pagina_professor(request):
    return render(request, 'professor.html')

@user_passes_test(lambda u: u.is_superuser)
def alterar_status(request, candidato_id):
    candidato = get_object_or_404(Candidato, id=candidato_id)
    
    if request.method == 'POST':
        aprovado = request.POST.get('status') == 'aprovar'
        candidato.aprovado = aprovado
        candidato.save()

    return redirect('lista_candidatos')

from django.shortcuts import render, redirect
from .models import Candidato

def verificar_aprovacao(request, candidato_id):
    candidato = Candidato.objects.get(id=candidato_id)
    
    if candidato.aprovado == aprovado:
        return render(request, 'aluno.html', {'candidato': candidato})
    else:
        return render(request, 'candidato_em_analise.html', {'candidato': candidato})
