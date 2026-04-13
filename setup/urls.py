from django.contrib import admin
from django.urls import path, include
from core.views import dashboard
from core.views import dashboard, cadastrar_tcc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),
    path('novo/', cadastrar_tcc, name='cadastrar_tcc'),
]