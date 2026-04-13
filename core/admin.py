from django.contrib import admin
from .models import Usuario, TrabalhoTCC, Entrega, Feedback, AtaOrientacao, Banca, ChecklistDocumental, CronogramaPrazo

admin.site.register(Usuario)
admin.site.register(TrabalhoTCC)
admin.site.register(Entrega)
admin.site.register(Feedback)
admin.site.register(AtaOrientacao)
admin.site.register(Banca)
admin.site.register(ChecklistDocumental)
admin.site.register(CronogramaPrazo)