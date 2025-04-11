from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path("logout/", views.logout_view, name="logout"),
    path("candidatos/", views.lista_candidatos, name="lista_candidatos"),
]
