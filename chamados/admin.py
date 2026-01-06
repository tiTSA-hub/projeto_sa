from django.contrib import admin
from django.utils.html import format_html
from .models import Chamado

# Esta é a configuração da tabela que você verá
class ChamadoAdmin(admin.ModelAdmin):
    # Aqui definimos as colunas EXATAS que vão aparecer na sua lista
    list_display = ('id', 'titulo', 'solicitante', 'setor', 'status', 'prioridade', 'ver_imagem')
    
    # Isso faz com que você mude o status sem precisar abrir o chamado
    list_editable = ('status', 'prioridade')
    
    # Isso cria a barra lateral de filtros que você já viu
    list_filter = ('setor', 'status', 'prioridade')
    
    # Isso cria a barra de busca
    search_fields = ('titulo', 'solicitante')

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