from django.db import models
from django.contrib.auth.models import User

class Chamado(models.Model):
    # Opções para a caixa suspensa
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
        ('Financeiro', 'Financeiro'),
        ('Juridico', 'Juridico'),
        ('Contabilidade', 'Contabilidade'),
        ('RH', 'RH'),
        ('Comercial', 'Comercial'),
        ('Operacional/Gate', 'Operacional/Gate'),
        ('Manutencao/Almoxarifado', 'Manutencao/Almoxarifado'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(verbose_name="Descrição do Problema")
    setor = models.CharField(max_length=50, choices=SETOR_CHOICES)
    ramal = models.CharField(max_length=10)
    solicitante = models.CharField(max_length=100)
    tecnico_responsavel = models.CharField(max_length=100, blank=True, null=True)
    
    # Aqui aplicamos o 'choices' para gerar a caixa suspensa no Admin
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='Baixa')
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='chamados/', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.titulo} ({self.solicitante})"

class Interacao(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='interacoes')
    agente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    texto = models.TextField(verbose_name="O que foi feito/Observações")
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Atendimento"
