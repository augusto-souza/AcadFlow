from django import forms
from .models import TrabalhoTCC, Entrega, Feedback, AtaOrientacao, Banca, ChecklistDocumental

# RF02 - Formulário para o Aluno propor o tema
class TrabalhoTCCForm(forms.ModelForm):
    class Meta:
        model = TrabalhoTCC
        fields = ['titulo', 'resumo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título do trabalho'}),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Breve resumo da proposta'}),
        }

# RF05/RF06 - Formulário para Upload de Arquivos (Entrega)
class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['arquivo', 'descricao']
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Versão Final, Correção Cap 1'}),
        }

# RF07 - Formulário para o Orientador dar Feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Insira as correções ou sugestões'}),
        }

# RF08 - Registro de Ata de Reunião
class AtaOrientacaoForm(forms.ModelForm):
    class Meta:
        model = AtaOrientacao
        fields = ['data_reuniao', 'resumo_discussao']
        widgets = {
            'data_reuniao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resumo_discussao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# RF09/RF13 - Agendamento de Banca e Lançamento de Notas
class BancaForm(forms.ModelForm):
    class Meta:
        model = Banca
        fields = ['data_defesa', 'local', 'avaliador_1', 'avaliador_2', 'avaliador_3', 'nota_1', 'nota_2', 'nota_3']
        widgets = {
            'data_defesa': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'avaliador_1': forms.Select(attrs={'class': 'form-select'}),
            'avaliador_2': forms.Select(attrs={'class': 'form-select'}),
            'avaliador_3': forms.Select(attrs={'class': 'form-select'}),
            'nota_1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'nota_2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'nota_3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

# RF12 - Verificação de Pendências Documentais
class ChecklistDocumentalForm(forms.ModelForm):
    class Meta:
        model = ChecklistDocumental
        fields = ['termo_autorizacao', 'nada_consta_biblioteca', 'versao_final_entregue']
        widgets = {
            'termo_autorizacao': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nada_consta_biblioteca': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'versao_final_entregue': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }