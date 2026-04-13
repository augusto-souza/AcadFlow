from django.db import models
from django.contrib.auth.models import AbstractUser

# RF01 - Gestão de Perfis e Acesso
class Usuario(AbstractUser):
    TIPOS = (
        ('ALUNO', 'Aluno'),
        ('ORIENTADOR', 'Orientador'),
        ('COORDENADOR', 'Coordenador'),
    )
    tipo = models.CharField(max_length=15, choices=TIPOS, default='ALUNO')

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


# RF02, RF03, RF04 - O projeto de TCC e Fluxo de Aceite
class TrabalhoTCC(models.Model):
    STATUS_CHOICES = (
        ('SUBMETIDO', 'Aguardando Aprovação'),
        ('ACEITO', 'Em Orientação'),
        ('REJEITADO', 'Proposta Rejeitada'),
        ('DEFESA_AGENDADA', 'Defesa Agendada'),
        ('CONCLUIDO', 'Concluído'),
    )

    titulo = models.CharField(max_length=255)
    resumo = models.TextField()
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='meus_tccs')
    orientador = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='orientacoes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMETIDO')
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # RF03 - Flag para o professor confirmar aceite
    aceite_orientador = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


# RF05, RF06 - Upload de Documentos e Versionamento
class Entrega(models.Model):
    trabalho = models.ForeignKey(TrabalhoTCC, on_delete=models.CASCADE, related_name='entregas')
    arquivo = models.FileField(upload_to='tccs/entregas/')
    descricao = models.CharField(max_length=100, help_text="Ex: Versão inicial, Cap 1, etc.")
    data_envio = models.DateTimeField(auto_now_add=True) # Registro de data/hora (Timestamp)

    def __str__(self):
        return f"Entrega: {self.descricao} - {self.trabalho.titulo}"


# RF07 - Módulo de Feedback
class Feedback(models.Model):
    entrega = models.OneToOneField(Entrega, on_delete=models.CASCADE, related_name='feedback')
    comentario = models.TextField()
    data_feedback = models.DateTimeField(auto_now_add=True)
    orientador = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback para {self.entrega.descricao}"


# RF08 - Registro de Orientação (Ata)
class AtaOrientacao(models.Model):
    trabalho = models.ForeignKey(TrabalhoTCC, on_delete=models.CASCADE, related_name='atas_reuniao')
    data_reuniao = models.DateField()
    resumo_discussao = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reunião {self.data_reuniao} - {self.trabalho.titulo}"


# RF09, RF13, RF14 - Agendamento de Bancas e Notas
class Banca(models.Model):
    trabalho = models.OneToOneField(TrabalhoTCC, on_delete=models.CASCADE, related_name='banca')
    data_defesa = models.DateTimeField()
    local = models.CharField(max_length=100)
    avaliador_1 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='banca_aval1')
    avaliador_2 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='banca_aval2')
    avaliador_3 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='banca_aval3')
    
    nota_1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota_2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota_3 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    media_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # RF13 - Cálculo automático da média final
        if self.nota_1 and self.nota_2 and self.nota_3:
            self.media_final = (self.nota_1 + self.nota_2 + self.nota_3) / 3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Banca de {self.trabalho.aluno.get_full_name()}"


# RF12 - Checklist Documental
class ChecklistDocumental(models.Model):
    trabalho = models.OneToOneField(TrabalhoTCC, on_delete=models.CASCADE, related_name='checklist')
    termo_autorizacao = models.BooleanField(default=False)
    nada_consta_biblioteca = models.BooleanField(default=False)
    versao_final_entregue = models.BooleanField(default=False)

    def __str__(self):
        return f"Checklist - {self.trabalho.titulo}"


# RF04 - Cronograma de Entregas (Datas-limite globais definidas pela coordenação)
class CronogramaPrazo(models.Model):
    descricao_etapa = models.CharField(max_length=100) # Ex: Entrega do Projeto, Entrega Final
    data_limite = models.DateTimeField()

    def __str__(self):
        return f"{self.descricao_etapa} até {self.data_limite}"