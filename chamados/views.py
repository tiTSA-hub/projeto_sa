from django.shortcuts import render, redirect
from .models import Chamado
from django.db.models import Count

def index(request):
    if request.method == 'POST':
        # Pegamos a imagem separadamente
        foto_enviada = request.FILES.get('imagem') 

        # Salva o chamado com todos os campos conforme o Models atualizado
        Chamado.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            setor=request.POST.get('setor'),
            ramal=request.POST.get('ramal'),
            solicitante=request.POST.get('solicitante'),
            imagem=foto_enviada 
            # Note que 'status' e 'prioridade' já têm valores default no model
        )
        return redirect('index')

    # Filtro: EXCLUDE retira os Concluídos da lista principal para não poluir o painel
    # Corrigido para 'Concluido' (sem acento) conforme definido no STATUS_CHOICES
    chamados = Chamado.objects.exclude(status='Concluido').order_by('-data_criacao')
    
    return render(request, 'index.html', {'chamados': chamados})

def dashboard(request):
    # Contadores para os Cards
    # Importante: Os nomes dos status aqui devem ser idênticos aos do Models.py
    total = Chamado.objects.count()
    pendentes = Chamado.objects.filter(status='Pendente').count()
    em_atendimento = Chamado.objects.filter(status='Em Andamento').count() # Ajustado de 'Em Atendimento' para 'Em Andamento'
    concluidos = Chamado.objects.filter(status='Concluido').count()

    # Dados para o Gráfico de Setores
    dados_setor = Chamado.objects.values('setor').annotate(total=Count('id'))
    labels = [item['setor'] for item in dados_setor]
    valores = [item['total'] for item in dados_setor]

    context = {
        'total': total,
        'pendentes': pendentes,
        'em_atendimento': em_atendimento,
        'concluidos': concluidos,
        'labels': labels,
        'valores': valores,
    }
    return render(request, 'dashboard.html', context)
