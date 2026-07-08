from django.contrib import admin
from django.urls import path
from credenciales import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.registro_credenciales, name='registro_credenciales'), # Pantalla principal
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'), # Descarga de Excel
    path('limpiar/', views.limpiar_registros, name='limpiar_registros'),   # PARA LIMPIAR LA TABLA
]