from django import forms
from .models import Candidato
from datetime import date

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'responsavel_data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_nasc = cleaned_data.get('data_nascimento')
        
        if data_nasc:
            # Cálculo temporário para validação
            hoje = date.today()
            idade = hoje.year - data_nasc.year - (
                (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day)
            )
            
            if idade < 18:
                campos_obrigatorios = ['responsavel_nome', 'responsavel_cpf']
                for campo in campos_obrigatorios:
                    if not cleaned_data.get(campo):
                        self.add_error(campo, "Campo obrigatório para menores de 18 anos")