from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, TrabalhoTCC

# Como estamos usando um modelo de usuário customizado, 
# usamos o UserAdmin para que os campos de senha funcionem direitinho
admin.site.register(Usuario, UserAdmin)

# Registra o modelo de TCC
admin.site.register(TrabalhoTCC)