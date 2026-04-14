from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('novo/', views.cadastrar_tcc, name='cadastrar_tcc'),
    path('tcc/<int:tcc_id>/', views.detalhes_tcc, name='detalhes_tcc'),
    path('tcc/<int:tcc_id>/entrega/', views.fazer_entrega, name='fazer_entrega'),
    path('tcc/<int:tcc_id>/ata/', views.registrar_ata, name='registrar_ata'),
    path('entrega/<int:entrega_id>/feedback/', views.dar_feedback, name='dar_feedback'),
    path('tcc/<int:tcc_id>/banca/', views.gerenciar_banca, name='gerenciar_banca'),
    path('tcc/<int:tcc_id>/pdf/', views.gerar_pdf_banca, name='gerar_pdf_banca'),
    path('signup/', views.signup, name='signup'),
]

# Configuração para que o Django consiga mostrar os arquivos de upload no navegador
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)