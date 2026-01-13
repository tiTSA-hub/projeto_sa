from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from chamados.views import index, dashboard  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  
    path('dashboard/', dashboard, name='dashboard'), 
]

# Configuração para servir arquivos de mídia e estáticos durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
