from django.db import models

class Chamado(models.Model):  # Certifique-se que o 'C' é maiúsculo!
    SETOR_CHOICES = [
        ('Diretoria', 'Diretoria'),
        ('Financeiro', 'Financeiro'),
        ('Juridico', 'Juridico'),
        ('Contabilidade', 'Contabilidade'),
        ('RH', 'RH'),
        ('Comercial', 'Comercial'),
        ('Operacional/Gate', 'Operacional/Gate'),
        ('Manutencao/Almoxarifado', 'Matutencao/Almoxarifado'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    setor = models.CharField(max_length=50, choices=SETOR_CHOICES)
    ramal = models.CharField(max_length=10)
    solicitante = models.CharField(max_length=100)
    tecnico_responsavel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pendente')
    prioridade = models.CharField(max_length=20, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='chamados/', null=True, blank=True)

    def __str__(self):
        return self.titulo