from django.db import models
from django.contrib.auth.models import User

class Chamado(models.Model):
# Caixa de suspensão (Dropdowmns)
    PRIORIDADE_CHOICES = [
        ('B', 'Baixa'),
        ('M', 'Média'),
        ('A', 'Alta'),
        ('U', 'Urgência'),
    ]
    STATUS_CHOICE = [
        ('P', 'Pendente'),
        ('E', 'Em Andamento'),
        ('C', 'Concluido'),
    ]
    
    SETOR_CHOICES = [
        ('Diretoria', 'Diretoria'),
        ('Financeiro', 'Financeiro'),
        ('Juridico', 'Juridico'),
        ('Contabilidade', 'Contabilidade'),
        ('RH', 'RH'),
        ('Comercial', 'Comercial'),
        ('Operacional/Gate', 'Operacional/Gate'),
        ('Manutencao/Almoxarifado', 'Manutencao/Almoxarifado'), # Corrigido aqui
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(verbose_name= "Descrição do Problema")
    setor = models.CharField(max_length=50, choices=SETOR_CHOICES)
    ramal = models.CharField(max_length=10)
    solicitante = models.CharField(max_length=100)
    tecnico_responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pendente')
    prioridade = models.CharField(max_length=20, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='chamados/', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.solicitante}"

# A caixa de diálogo do que foi  feito (interaçções)
class Interacao(models.Models):
    chamado = models.ForeignKey (Chamado, on_delete=models.CASCADE, related_name='interacoes')
    agente = models.ForeignKey (User, on_delete=models.SET_NULL, null=True)
    texto = models.TextField (verbose_name="O que foi feito/Obsevações")
    data_registro= models.DateTimeField(auto_now_add= True)

    class Meta:
        verbose_name = "Histórico de Atendimento"
