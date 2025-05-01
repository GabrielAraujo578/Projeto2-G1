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
    path('candidatos/<int:candidato_id>/status/', views.alterar_status, name='alterar_status'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('confirmacao_email/', views.confirmacao_email_view, name='confirmacao_email'),
    path('avisos/', views.lista_avisos, name='lista_avisos'),
    path('avisos/criar/', views.criar_aviso, name='criar_aviso'),
    path('calendario/', views.calendario, name='calendario'),
    path('adicionar-evento/', views.adicionar_evento, name='adicionar_evento'),
    path('evento/<int:id>/', views.detalhe_evento, name='detalhe_evento'),
    path('evento/<int:id>/editar/', views.editar_evento, name='editar_evento'),
    path('chat/aluno/', views.chat_aluno, name='chat_aluno'),
    path('chat/professor/', views.lista_chats, name='lista_chats'),
    path('chat/professor/<int:aluno_id>/', views.chat_professor, name='chat_professor'), 
]