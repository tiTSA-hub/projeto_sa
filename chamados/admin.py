from django.contrib import admin
from django.utils.html import format_html
from .models import Chamado, Interacao

class InteracaoInline(admin.TabularInline):
    model = Interacao
    extra = 1

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'solicitante', 'tecnico_responsavel', 'setor', 'status', 'sala_selecionada', 'data_reserva', 'ver_imagem')
    list_editable = ('status', 'tecnico_responsavel')
    list_filter = ('status', 'setor', 'sala_selecionada')
    inlines = [InteracaoInline]

    def ver_imagem(self, obj):
        if obj.imagem:
            return format_html('<a href="{}" target="_blank">🖼️ VER</a>', obj.imagem.url)
        return "-"
    ver_imagem.short_description = "Print"