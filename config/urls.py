from django.contrib import admin
from django.urls import path
from credenciales import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'), # Pantalla de bienvenida vacía
    path('credenciales/', views.registro_credenciales, name='registro_credenciales'), # Solo aquí sale el formulario y la tabla
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'), # Descarga de Excel
    path('limpiar/', views.limpiar_registros, name='limpiar_registros'),   # Limpiar la tabla
]