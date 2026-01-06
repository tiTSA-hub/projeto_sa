from django.shortcuts import render, redirect
from .models import Chamado
from django.db.models import Count

def index(request):
    if request.method == 'POST':
        # Pegamos a imagem separadamente
        foto_enviada = request.FILES.get('imagem') 

        # Salva o chamado com todos os campos
        Chamado.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            setor=request.POST.get('setor'),
            ramal=request.POST.get('ramal'),
            solicitante=request.POST.get('solicitante'), # Faltava a vírgula aqui
            imagem=foto_enviada # Salvando o arquivo no campo certo
        )
        return redirect('index')

    # Filtro: EXCLUDE retira os Concluídos da lista automaticamente
    chamados = Chamado.objects.exclude(status='Concluido').order_by('-data_criacao')
    
    return render(request, 'index.html', {'chamados': chamados})

def dashboard(request):
 from django.db.models import Count # Verifique se esta linha está no topo

def dashboard(request):
    # Contadores para os Cards (o que aparece no topo)
    total = Chamado.objects.count()
    pendentes = Chamado.objects.filter(status='Pendente').count()
    em_atendimento = Chamado.objects.filter(status='Em Atendimento').count()
    concluidos = Chamado.objects.filter(status='Concluido').count()

    # Dados para o Gráfico de Setores (o que já tínhamos)
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