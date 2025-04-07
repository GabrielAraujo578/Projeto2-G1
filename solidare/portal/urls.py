from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal, name='portal'),
]