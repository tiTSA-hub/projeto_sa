from django.contrib import admin
from django.utils.html import format_html
from .models import Chamado, Interacao

class InteracaoInline(admin.TabularInline):
    model = Interacao
    extra = 1
    readonly_fields = ('data_registro', 'agente')

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    # Colunas visíveis na lista
    list_display = ('id', 'titulo', 'solicitante', 'tecnico_responsavel', 'setor', 'status', 'prioridade', 'ver_imagem')
    
    # PRATICIDADE: O técnico edita status, prioridade e técnico direto na lista!
    list_editable = ('status', 'prioridade', 'tecnico_responsavel')
    
    # Filtros laterais para facilitar a gestão
    list_filter = ('status', 'prioridade', 'setor', 'tecnico_responsavel')
    
    # Barra de busca
    search_fields = ('titulo', 'solicitante', 'tecnico_responsavel')

    # Histórico de atendimento dentro do chamado
    inlines = [InteracaoInline]

    # Atribuição automática de técnico ao mudar para 'Em Andamento'
    def save_model(self, request, obj, form, change):
        if obj.status == 'Em Andamento' and not obj.tecnico_responsavel:
            obj.tecnico_responsavel = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)

    # Link para visualizar imagem anexada
    def ver_imagem(self, obj):
        if obj.imagem:
            return format_html('<a href="{}" target="_blank" style="font-weight:bold; color:#cc0000;">🖼️ VER PRINT</a>', obj.imagem.url)
        return "Sem anexo"
    
    ver_imagem.short_description = 'Anexo'

# Registrar Interação separadamente se necessário
admin.site.register(Interacao)
