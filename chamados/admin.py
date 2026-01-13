from django.contrib import admin
from django.utils.html import format_html
from .models import Chamado, Interacao

class InteracaoInline(admin.TabularInLine):
    models = Interacao
    extra = 1
    readonly_fields = ('data_registro', 'agente')

# Esta é a configuração da tabela que você verá
@admin.rester(Chamados)
class ChamadoAdmin(admin.ModelAdmin):
    # Aqui definimos as colunas EXATAS que vão aparecer na sua lista
    list_display = ('id', 'titulo', 'solicitante', 'agente_responsavel', 'setor', 'status', 'prioridade', 'ver_imagem')
    
    # Isso faz com que você mude o status sem precisar abrir o chamado
    list_editable = ('status', 'prioridade')
    
    # Isso cria a barra lateral de filtros que você já viu
    list_filter = ('setor', 'status', 'prioridade', 'agente_responsavel')
    
    # Isso cria a barra de busca
    search_fields = ('titulo', 'solicitante', 'descricao','usuario_solicitante', 'agente_responsavel', 'status', 'prioridade')

    inlines = [InteracaoInLine]

    def save_model(self,request, obj, form, change):
        if obj.status == 'E' and not obj.agente_responsavel:
            obj.agente_responsavel = requeste.user
        super().save_model(request, obj, form, change)
        

    # Esta função cria o link para você ver o print do erro
    def ver_imagem(self, obj):
        if obj.imagem:
            return format_html('<a href="{}" target="_blank" style="font-weight:bold; color:#cc0000;">🖼️ VER PRINT</a>', obj.imagem.url)
        return "Sem anexo"
    
    ver_imagem.short_description = 'Anexo' # Nome da coluna

# Se já houver um registro, vamos limpar e registrar do jeito certo
if admin.site.is_registered(Chamado):
    admin.site.unregister(Chamado)

admin.site.register(Chamado, ChamadoAdmin)
