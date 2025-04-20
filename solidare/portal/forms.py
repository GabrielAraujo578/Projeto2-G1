from django import forms
from django.contrib.auth.models import User
from .models import Candidato
from django.contrib.auth.hashers import make_password
from datetime import date


class CandidatoForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirme a senha")

    class Meta:
        model = Candidato
        exclude = ['idade', 'aprovado', 'user']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'responsavel_data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data_nasc = cleaned_data.get('data_nascimento')

        if data_nasc:
            hoje = date.today()
            idade = hoje.year - data_nasc.year - (
                (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day)
            )
            if idade < 18:
                for campo in ['responsavel_nome', 'responsavel_cpf']:
                    if not cleaned_data.get(campo):
                        self.add_error(campo, "Campo obrigatório para menores de 18 anos")

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "As senhas não coincidem.")

        return cleaned_data

    def save(self, commit=True):
        # Não cria o user aqui! Só salva o Candidato.
        candidato = super().save(commit=False)
        return candidato