from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.template.loader import get_template
from .models import TrabalhoTCC, Entrega, Feedback, AtaOrientacao, Banca, ChecklistDocumental
from .forms import (
    TrabalhoTCCForm, EntregaForm, FeedbackForm, 
    AtaOrientacaoForm, BancaForm, ChecklistDocumentalForm,
    UsuarioCadastroForm  # Adicionado para o autocadastro
)

# Bibliotecas para PDF e Tempo
import io
import datetime
from xhtml2pdf import pisa

# --- AUTENTICAÇÃO E REGISTRO ---

def signup(request):
    """View para criação de novas contas (RF01)"""
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UsuarioCadastroForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- DASHBOARD PRINCIPAL ---

@login_required
def dashboard(request):
    # Se for Aluno, vê apenas os seus TCCs. Se for Orientador/Coordenador, vê todos.
    if request.user.tipo == 'ALUNO':
        trabalhos = TrabalhoTCC.objects.filter(aluno=request.user)
    else:
        trabalhos = TrabalhoTCC.objects.all()
        
    return render(request, 'core/dashboard.html', {'trabalhos': trabalhos})

# --- GESTÃO DE TCC (PROPOSTA) ---

@login_required
def cadastrar_tcc(request):
    if request.method == 'POST':
        form = TrabalhoTCCForm(request.POST)
        if form.is_valid():
            tcc = form.save(commit=False)
            tcc.aluno = request.user
            tcc.save()
            return redirect('dashboard')
    else:
        form = TrabalhoTCCForm()
    return render(request, 'core/form_tcc.html', {'form': form})

# --- ENTREGAS E VERSIONAMENTO (RF05/RF06) ---

@login_required
def fazer_entrega(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    if request.method == 'POST':
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.trabalho = tcc
            entrega.save()
            return redirect('detalhes_tcc', tcc_id=tcc.id)
    else:
        form = EntregaForm()
    return render(request, 'core/form_entrega.html', {'form': form, 'tcc': tcc})

# --- FEEDBACK DO ORIENTADOR (RF07) ---

@login_required
def dar_feedback(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.entrega = entrega
            feedback.orientador = request.user
            feedback.save()
            return redirect('detalhes_tcc', tcc_id=entrega.trabalho.id)
    else:
        form = FeedbackForm()
    return render(request, 'core/form_feedback.html', {'form': form, 'entrega': entrega})

# --- REGISTRO DE ATAS (RF08) ---

@login_required
def registrar_ata(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    if request.method == 'POST':
        form = AtaOrientacaoForm(request.POST)
        if form.is_valid():
            ata = form.save(commit=False)
            ata.trabalho = tcc
            ata.save()
            return redirect('detalhes_tcc', tcc_id=tcc.id)
    else:
        form = AtaOrientacaoForm()
    return render(request, 'core/form_ata.html', {'form': form, 'tcc': tcc})

# --- PÁGINA DE DETALHES DO TCC ---

@login_required
def detalhes_tcc(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    entregas = tcc.entregas.all().order_by('-data_envio')
    atas = tcc.atas_reuniao.all().order_by('-data_reuniao')
    return render(request, 'core/detalhes_tcc.html', {
        'tcc': tcc,
        'entregas': entregas,
        'atas': atas
    })

# --- GERENCIAR BANCA E NOTAS (RF09/RF13) ---

@login_required
def gerenciar_banca(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    banca, created = Banca.objects.get_or_create(trabalho=tcc)
    
    if request.method == 'POST':
        form = BancaForm(request.POST, instance=banca)
        if form.is_valid():
            form.save()
            if banca.media_final:
                tcc.status = 'CONCLUIDO'
                tcc.save()
            return redirect('detalhes_tcc', tcc_id=tcc.id)
    else:
        form = BancaForm(instance=banca)
    
    return render(request, 'core/form_banca.html', {'form': form, 'tcc': tcc})

# --- GERAR PDF DA ATA (RF14) ---

@login_required
def gerar_pdf_banca(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    banca = getattr(tcc, 'banca', None)

    if not banca:
        return redirect('detalhes_tcc', tcc_id=tcc.id)

    context = {
        'tcc': tcc,
        'banca': banca,
        'data_atual': datetime.datetime.now(),
    }

    template = get_template('core/pdf_banca.html')
    html = template.render(context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=f'Ata_Defesa_{tcc.aluno.username}.pdf')
    
    return redirect('detalhes_tcc', tcc_id=tcc.id)