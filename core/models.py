from django.db import models
from django.contrib.auth.models import AbstractUser

# --- RF01: GESTÃO DE PERFIS E ACESSO ---
class Usuario(AbstractUser):
    TIPOS = (
        ('ALUNO', 'Aluno'),
        ('ORIENTADOR', 'Orientador'),
        ('COORDENADOR', 'Coordenador'),
    )
    tipo = models.CharField(max_length=15, choices=TIPOS, default='ALUNO')

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_tipo_display()})"


# --- RF02, RF03: TRABALHO DE CONCLUSÃO DE CURSO ---
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
    
    # Flag para controle de aceite do orientador ou atribuição pela coordenação
    aceite_orientador = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


# --- RF05, RF06: ENTREGAS E VERSIONAMENTO ---
class Entrega(models.Model):
    trabalho = models.ForeignKey(TrabalhoTCC, on_delete=models.CASCADE, related_name='entregas')
    arquivo = models.FileField(upload_to='tccs/entregas/')
    descricao = models.CharField(max_length=100, help_text="Ex: Versão inicial, Cap 1, etc.")
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descricao} - {self.trabalho.titulo}"


# --- RF07: MÓDULO DE FEEDBACK (Ajustado para respostas encadeadas) ---
class Feedback(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='feedbacks')
    comentario = models.TextField()
    data_feedback = models.DateTimeField(auto_now_add=True)
    
    # Renomeado para 'autor' para permitir que alunos também respondam
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    # Campo autorreferencial para permitir respostas em cima de feedbacks
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respostas')

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.data_feedback.strftime('%d/%m/%Y')}"


# --- RF08: REGISTRO DE ORIENTAÇÃO (ATA) ---
class AtaOrientacao(models.Model):
    trabalho = models.ForeignKey(TrabalhoTCC, on_delete=models.CASCADE, related_name='atas_reuniao')
    data_reuniao = models.DateField()
    resumo_discussao = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reunião {self.data_reuniao} - {self.trabalho.titulo}"


# --- RF09, RF13, RF14: BANCA, NOTAS E MÉDIA ---
class Banca(models.Model):
    trabalho = models.OneToOneField(TrabalhoTCC, on_delete=models.CASCADE, related_name='banca')
    
    data_defesa = models.DateTimeField(null=True, blank=True)
    local = models.CharField(max_length=100, null=True, blank=True)
    
    avaliador_1 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='banca_aval1')
    avaliador_2 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='banca_aval2')
    avaliador_3 = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='banca_aval3')
    
    nota_1 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota_2 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nota_3 = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    media_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.nota_1 is not None and self.nota_2 is not None and self.nota_3 is not None:
            self.media_final = (self.nota_1 + self.nota_2 + self.nota_3) / 3
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Banca de {self.trabalho.aluno.username}"


# --- RF12: CHECKLIST DOCUMENTAL ---
class ChecklistDocumental(models.Model):
    trabalho = models.OneToOneField(TrabalhoTCC, on_delete=models.CASCADE, related_name='checklist')
    termo_autorizacao = models.BooleanField(default=False)
    nada_consta_biblioteca = models.BooleanField(default=False)
    versao_final_entregue = models.BooleanField(default=False)

    def __str__(self):
        return f"Checklist - {self.trabalho.titulo}"


# --- RF04: CRONOGRAMA DE PRAZOS GLOBAIS ---
class CronogramaPrazo(models.Model):
    descricao_etapa = models.CharField(max_length=100)
    data_limite = models.DateTimeField()

    def __str__(self):
        return f"{self.descricao_etapa} - {self.data_limite.strftime('%d/%m/%Y')}"