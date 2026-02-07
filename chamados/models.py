from django.db import models
from django.contrib.auth.models import User

class Chamado(models.Model):
    PRIORIDADE_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
        ('Urgência', 'Urgência'),
    ]
    
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em Andamento', 'Em Andamento'),
        ('Concluido', 'Concluido'),
    ]
    
    SETOR_CHOICES = [
        ('Diretoria', 'Diretoria'),
        ('Juridico', 'Jurídico'),
        ('Financeiro', 'Financeiro'),
        ('Compras', 'Compras'),
        ('Contabilidade', 'Contabilidade'),
        ('Capital Humano', 'Capital Humano'),
        ('Comercial', 'Comercial'),
        ('Operacional/Gate', 'Operacional/Gate'),
        ('Manutencao/Almoxarifado', 'Manutenção/Almoxarifado'),
    ]

    SALA_CHOICES = [
        ('nenhuma', 'Nenhuma (Apenas chamado)'),
        ('Sala 01', 'Sala de Reunião 01'),
        ('Sala 02', 'Sala de Reunião 02'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(verbose_name="Descrição/Pauta", blank=True, null=True)
    setor = models.CharField(max_length=50, choices=SETOR_CHOICES)
    ramal = models.CharField(max_length=20) 
    solicitante = models.CharField(max_length=100)
    tecnico_responsavel = models.CharField(max_length=100, blank=True, null=True, default="Aguardando...")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='Baixa')
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='chamados/', null=True, blank=True)

    # Campos de Reserva
    sala_selecionada = models.CharField(max_length=20, choices=SALA_CHOICES, default='nenhuma')
    data_reserva = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fim = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.solicitante})"

class Interacao(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='interacoes')
    agente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    texto = models.TextField(verbose_name="Observações")
    data_registro = models.DateTimeField(auto_now_add=True)