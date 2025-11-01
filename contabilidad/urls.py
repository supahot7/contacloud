from django.urls import path
from . import views

app_name = 'contabilidad'  # namespace para usar en templates y reverse()

urlpatterns = [
    path('panel/', views.panel_principal, name='panel_principal'),
    path('catalogo/', views.catalogo_cuentas, name='catalogo_cuentas'),
]
