from django.contrib import admin
from django.utils.html import format_html
from .models import Chamado, Interacao

# Configuração para escrever o que foi feito dentro do chamado
class InteracaoInline(admin.TabularInline): # Corrigido: TabularInline
    model = Interacao # Corrigido: model (no singular)
    extra = 1
    readonly_fields = ('data_registro', 'agente')

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    # Colunas da lista principal
    # Usei 'tecnico_responsavel' para bater com seu models.py
    list_display = ('id', 'titulo', 'solicitante', 'tecnico_responsavel', 'setor', 'status', 'prioridade', 'ver_imagem')
    
    # Edição rápida na lista
    list_editable = ('status', 'prioridade')
    
    # Filtros laterais
    list_filter = ('setor', 'status', 'prioridade', 'tecnico_responsavel')
    
    # Barra de busca
    search_fields = ('titulo', 'solicitante', 'descricao', 'tecnico_responsavel')

    # Inclui a caixa de interação dentro do chamado
    inlines = [InteracaoInline]

    # Lógica para atribuir o técnico automaticamente ao mudar status
    def save_model(self, request, obj, form, change):
        # Se status for 'Em Andamento' e não tiver técnico, assume o usuário logado
        if obj.status == 'Em Andamento' and not obj.tecnico_responsavel:
            obj.tecnico_responsavel = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)

    # Função para exibir o link da imagem
    def ver_imagem(self, obj):
        if obj.imagem:
            return format_html('<a href="{}" target="_blank" style="font-weight:bold; color:#cc0000;">🖼️ VER PRINT</a>', obj.imagem.url)
        return "Sem anexo"
    
    ver_imagem.short_description = 'Anexo'

# Registro da Interação separada também (opcional)
admin.site.register(Interacao)
