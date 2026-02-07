from django.shortcuts import render, redirect
from .models import Chamado
from django.db.models import Count, Q
from django.contrib import messages
from django.utils import timezone

def index(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        setor = request.POST.get('setor')
        solicitante = request.POST.get('solicitante')
        ramal = request.POST.get('ramal')
        descricao = request.POST.get('descricao', '')
        foto = request.FILES.get('imagem')
        sala = request.POST.get('sala_selecionada')
        data_res = request.POST.get('data_reserva')
        h_ini = request.POST.get('hora_inicio')
        h_fim = request.POST.get('hora_fim')

        if sala != 'nenhuma' and data_res:
            if not h_ini or not h_fim:
                messages.error(request, "Selecione o horário para a reserva.")
                return redirect('index')

            conflito = Chamado.objects.filter(
                sala_selecionada=sala, data_reserva=data_res,
                hora_inicio__lt=h_fim, hora_fim__gt=h_ini
            ).exists()

            if conflito and setor != 'Diretoria':
                messages.error(request, f"A {sala} já está ocupada neste horário.")
                return redirect('index')
            elif conflito and setor == 'Diretoria':
                messages.warning(request, "Reserva realizada com prioridade da Diretoria.")

        Chamado.objects.create(
            titulo=titulo, setor=setor, solicitante=solicitante, ramal=ramal,
            descricao=descricao, imagem=foto, sala_selecionada=sala,
            data_reserva=data_res if data_res else None,
            hora_inicio=h_ini if h_ini else None,
            hora_fim=h_fim if h_fim else None
        )
        messages.success(request, "Solicitação enviada!")
        return redirect('index')

    chamados = Chamado.objects.exclude(status='Concluido').order_by('-data_criacao')
    return render(request, 'index.html', {'chamados': chamados})

def dashboard(request):
    agora, hoje = timezone.localtime().time(), timezone.localtime().date()
    context = {
        'total': Chamado.objects.count(),
        'pendentes': Chamado.objects.filter(status='Pendente').count(),
        'em_atendimento': Chamado.objects.filter(status='Em Andamento').count(),
        'concluidos': Chamado.objects.filter(status='Concluido').count(),
        'sala1_ocupada': Chamado.objects.filter(sala_selecionada='Sala 01', data_reserva=hoje, hora_inicio__lte=agora, hora_fim__gte=agora).exists(),
        'sala2_ocupada': Chamado.objects.filter(sala_selecionada='Sala 02', data_reserva=hoje, hora_inicio__lte=agora, hora_fim__gte=agora).exists(),
    }
    dados = Chamado.objects.values('setor').annotate(total=Count('id'))
    context['labels'] = [d['setor'] for d in dados]
    context['valores'] = [d['total'] for d in dados]
    return render(request, 'dashboard.html', context)