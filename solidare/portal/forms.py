from django import forms
from .models import Candidato

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__' 
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'responsavel_data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
