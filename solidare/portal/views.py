from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CandidatoForm  
from .models import Candidato 

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redireciona para a home (pode ajustar)
        else:
            return render(request, "login.html", {"erro": "Usuário ou senha inválidos"})
    return render(request, "login.html")

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
    return render(request, "index.html")  # Renderiza a página inicial

def lista_candidatos(request):
    # Aqui você pode adicionar lógica depois, como buscar candidatos do banco
    return render(request, "lista_candidatos.html")

def cadastro_candidato(request):
    if request.method == "POST":
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_candidatos")
    else:
        form = CandidatoForm()
    return render(request, "cadastro_candidato.html", {"form": form})