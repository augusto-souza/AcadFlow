from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, TrabalhoTCC, Entrega, Feedback, AtaOrientacao, Banca, ChecklistDocumental

# --- FUNÇÃO AUXILIAR PARA ESTILIZAR ---
def aplicar_bootstrap(fields):
    """Aplica as classes do Bootstrap automaticamente baseada no tipo de campo"""
    for field_name, field in fields.items():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs['class'] = 'form-check-input'
        elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
            field.widget.attrs['class'] = 'form-select'
        else:
            field.widget.attrs['class'] = 'form-control'

# --- FORMULÁRIOS ---

class UsuarioCadastroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'tipo')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)

class TrabalhoTCCForm(forms.ModelForm):
    class Meta:
        model = TrabalhoTCC
        fields = ['titulo', 'resumo']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Digite o título do trabalho'}),
            'resumo': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Breve resumo da proposta'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['arquivo', 'descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Ex: Versão Final, Correção Cap 1'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Insira as correções ou sugestões'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)

class AtaOrientacaoForm(forms.ModelForm):
    class Meta:
        model = AtaOrientacao
        fields = ['data_reuniao', 'resumo_discussao']
        widgets = {
            'data_reuniao': forms.DateInput(attrs={'type': 'date'}),
            'resumo_discussao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descreva o que foi discutido na reunião...'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)

class BancaForm(forms.ModelForm):
    class Meta:
        model = Banca
        fields = ['data_defesa', 'local', 'avaliador_1', 'avaliador_2', 'avaliador_3', 'nota_1', 'nota_2', 'nota_3']
        widgets = {
            'data_defesa': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)

class ChecklistDocumentalForm(forms.ModelForm):
    class Meta:
        model = ChecklistDocumental
        fields = ['termo_autorizacao', 'nada_consta_biblioteca', 'versao_final_entregue']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_bootstrap(self.fields)