from django.urls import path
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('panel/', views.panel_principal, name='panel_principal'),
    path('catalogo/', views.catalogo_cuentas, name='catalogoCuentas'),
    
]

