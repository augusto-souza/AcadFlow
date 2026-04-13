from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TrabalhoTCC


@login_required
def dashboard(request):
    trabalhos = TrabalhoTCC.objects.all()
    return render(request, 'core/dashboard.html', {'trabalhos': trabalhos})

@login_required
def cadastrar_tcc(request):
    if request.method == 'POST':
        form = TrabalhoTCCForm(request.POST)
        if form.is_valid():
            tcc = form.save(commit=False)
            tcc.aluno = request.user  # Vincula o TCC ao usuário logado
            tcc.save()
            return redirect('dashboard')
    else:
        form = TrabalhoTCCForm()
    return render(request, 'core/form_tcc.html', {'form': form})