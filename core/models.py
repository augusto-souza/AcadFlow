from django.db import models
from django.contrib.auth.models import AbstractUser

# RF01 - Customizando o usuário para ter níveis de acesso
class Usuario(AbstractUser):
    TIPOS = (
        ('ALUNO', 'Aluno'),
        ('ORIENTADOR', 'Orientador'),
        ('COORDENADOR', 'Coordenador'),
    )
    tipo = models.CharField(max_length=15, choices=TIPOS, default='ALUNO')

# RF02 - O projeto de TCC em si
class TrabalhoTCC(models.Model):
    STATUS_CHOICES = (
        ('SUBMETIDO', 'Aguardando Aprovação'),
        ('EM_ANDAMENTO', 'Em Orientação'),
        ('CONCLUIDO', 'Concluído'),
    )
    
    titulo = models.CharField(max_length=255)
    resumo = models.TextField()
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='meu_tcc')
    orientador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='orientacoes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMETIDO')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo