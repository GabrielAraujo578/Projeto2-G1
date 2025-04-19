from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('candidato/cadastro/', views.cadastro_candidato, name='cadastro_candidato'),
    path('candidatos/', views.lista_candidatos, name='lista_candidatos'),
    path("cadastro/sucesso/", views.cadastro_sucesso, name="cadastro_sucesso"),
    path('aluno/', views.pagina_aluno, name='pagina_aluno'),
    path('professor/', views.pagina_professor, name='pagina_professor'),
]