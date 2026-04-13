from django import forms
from .models import TrabalhoTCC

class TrabalhoTCCForm(forms.ModelForm):
    class Meta:
        model = TrabalhoTCC
        fields = ['titulo', 'resumo'] # O aluno só preenche isso
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }