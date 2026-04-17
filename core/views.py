from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.template.loader import get_template
from .models import (
    Usuario, TrabalhoTCC, Entrega, Feedback, 
    AtaOrientacao, Banca, ChecklistDocumental, CronogramaPrazo
)
from .forms import (
    UsuarioCadastroForm, TrabalhoTCCForm, EntregaForm, 
    FeedbackForm, AtaOrientacaoForm, BancaForm, 
    ChecklistDocumentalForm, CronogramaPrazoForm
)

# Bibliotecas para PDF e Tempo
import io
import datetime
from xhtml2pdf import pisa

# --- 1. AUTENTICAÇÃO E REGISTRO ---

def signup(request):
    """Permite que novos usuários criem suas contas (RF01)"""
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioCadastroForm()
    return render(request, 'registration/signup.html', {'form': form})


# --- 2. DASHBOARD E CRONOGRAMA ---

@login_required
def dashboard(request):
    """Página principal com lista de TCCs e Prazos Globais (RF04)"""
    if request.user.tipo == 'ALUNO':
        trabalhos = TrabalhoTCC.objects.filter(aluno=request.user)
    else:
        trabalhos = TrabalhoTCC.objects.all()
    
    prazos = CronogramaPrazo.objects.all().order_by('data_limite')
    
    return render(request, 'core/dashboard.html', {
        'trabalhos': trabalhos,
        'prazos': prazos
    })

@login_required
def gerenciar_cronograma(request):
    """Permite ao Coordenador definir prazos para todo o sistema"""
    if request.user.tipo != 'COORDENADOR':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CronogramaPrazoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CronogramaPrazoForm()
    return render(request, 'core/form_cronograma.html', {'form': form})


# --- 3. FLUXO DO TCC (PROPOSTA E DETALHES) ---

@login_required
def cadastrar_tcc(request):
    """Aluno submete nova proposta (RF02)"""
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

@login_required
def detalhes_tcc(request, tcc_id):
    """Visão completa do projeto, entregas e atas"""
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    ChecklistDocumental.objects.get_or_create(trabalho=tcc)
    entregas = tcc.entregas.all().order_by('-data_envio')
    atas = tcc.atas_reuniao.all().order_by('-data_reuniao')
    return render(request, 'core/detalhes_tcc.html', {
        'tcc': tcc,
        'entregas': entregas,
        'atas': atas
    })

@login_required
def deletar_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    tcc_id = feedback.entrega.trabalho.id
    
    # Segurança: Só deleta se o usuário logado for o dono do feedback
    if request.user == feedback.orientador:
        feedback.delete()
    
    return redirect('detalhes_tcc', tcc_id=tcc_id)

@login_required
def deletar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    tcc_id = entrega.trabalho.id
    
    # Segurança: Apenas o aluno dono do TCC pode deletar a entrega
    if request.user == entrega.trabalho.aluno:
        # Nota: O Django não deleta o arquivo físico da pasta media automaticamente 
        # ao deletar o objeto, mas remove a referência no banco.
        entrega.delete()
    
    return redirect('detalhes_tcc', tcc_id=tcc_id)

@login_required
def atribuir_orientador(request, tcc_id):
    """Coordenador define quem orientará o projeto"""
    if request.user.tipo != 'COORDENADOR':
        return redirect('dashboard')
    
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    if request.method == 'POST':
        orientador_id = request.POST.get('orientador')
        tcc.orientador_id = orientador_id
        tcc.aceite_orientador = True
        tcc.status = 'ACEITO'
        tcc.save()
        return redirect('detalhes_tcc', tcc_id=tcc.id)
    
    orientadores = Usuario.objects.filter(tipo='ORIENTADOR')
    return render(request, 'core/atribuir_orientador.html', {
        'tcc': tcc, 
        'orientadores': orientadores
    })

@login_required
def deletar_tcc(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    
    # Segurança: Apenas o aluno dono da proposta pode deletar
    if request.user == tcc.aluno:
        tcc.delete()
    
    return redirect('dashboard')

# --- 4. ENTREGAS E FEEDBACKS (RF05, RF06, RF07) ---

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

@login_required
def dar_feedback(request, entrega_id):
    """Permite múltiplos feedbacks por entrega"""
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

@login_required
def editar_feedback(request, feedback_id):
    """Orientador edita um feedback já postado"""
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    if request.user != feedback.orientador:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('detalhes_tcc', tcc_id=feedback.entrega.trabalho.id)
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'core/form_feedback.html', {
        'form': form, 
        'entrega': feedback.entrega, 
        'editando': True
    })


# --- 5. ATAS, BANCA E DOCUMENTAÇÃO (RF08, RF09, RF12) ---

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

@login_required
def gerenciar_checklist(request, tcc_id):
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    checklist, created = ChecklistDocumental.objects.get_or_create(trabalho=tcc)
    if request.method == 'POST':
        form = ChecklistDocumentalForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            return redirect('detalhes_tcc', tcc_id=tcc.id)
    else:
        form = ChecklistDocumentalForm(instance=checklist)
    return render(request, 'core/form_checklist.html', {'form': form, 'tcc': tcc})

@login_required
def gerar_pdf_banca(request, tcc_id):
    """Gera ata oficial em PDF (RF14)"""
    tcc = get_object_or_404(TrabalhoTCC, pk=tcc_id)
    banca = getattr(tcc, 'banca', None)
    if not banca:
        return redirect('detalhes_tcc', tcc_id=tcc.id)
    
    context = {'tcc': tcc, 'banca': banca, 'data_atual': datetime.datetime.now()}
    template = get_template('core/pdf_banca.html')
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        result.seek(0)
        return FileResponse(result, as_attachment=True, filename=f'Ata_Defesa_{tcc.aluno.username}.pdf')
    return redirect('detalhes_tcc', tcc_id=tcc.id)

@login_required
def dar_feedback(request, entrega_id, parent_id=None):
    entrega = get_object_or_404(Entrega, pk=entrega_id)
    parent = None
    if parent_id:
        parent = get_object_or_404(Feedback, pk=parent_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.entrega = entrega
            feedback.autor = request.user
            feedback.parent = parent # Vincula ao comentário "pai" se existir
            feedback.save()
            return redirect('detalhes_tcc', tcc_id=entrega.trabalho.id)
    else:
        form = FeedbackForm()
        
    return render(request, 'core/form_feedback.html', {'form': form, 'entrega': entrega})

@login_required
def editar_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    
    # Segurança: Apenas o autor original pode editar o seu comentário
    if request.user != feedback.autor:
        return redirect('detalhes_tcc', tcc_id=feedback.entrega.trabalho.id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('detalhes_tcc', tcc_id=feedback.entrega.trabalho.id)
    else:
        # O instance=feedback faz com que o formulário já venha com o texto atual
        form = FeedbackForm(instance=feedback)
    
    return render(request, 'core/form_feedback.html', {
        'form': form, 
        'entrega': feedback.entrega, 
        'editando': True
    })