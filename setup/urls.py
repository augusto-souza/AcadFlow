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
    path('tcc/<int:tcc_id>/checklist/', views.gerenciar_checklist, name='gerenciar_checklist'),
    path('cronograma/', views.gerenciar_cronograma, name='gerenciar_cronograma'),
    path('tcc/<int:tcc_id>/checklist/', views.gerenciar_checklist, name='gerenciar_checklist'),
    path('feedback/editar/<int:feedback_id>/', views.editar_feedback, name='editar_feedback'), # Aproveite e adicione esta
    path('tcc/<int:tcc_id>/atribuir/', views.atribuir_orientador, name='atribuir_orientador'),
    path('feedback/deletar/<int:feedback_id>/', views.deletar_feedback, name='deletar_feedback'),
    path('entrega/deletar/<int:entrega_id>/', views.deletar_entrega, name='deletar_entrega'),
    path('tcc/deletar/<int:tcc_id>/', views.deletar_tcc, name='deletar_tcc'),
    path('entrega/<int:entrega_id>/feedback/', views.dar_feedback, name='dar_feedback'),
    path('entrega/<int:entrega_id>/feedback/<int:parent_id>/', views.dar_feedback, name='responder_feedback'),
    path('feedback/editar/<int:feedback_id>/', views.editar_feedback, name='editar_feedback'), # E esta
]

# Configuração para que o Django consiga mostrar os arquivos de upload no navegador
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)