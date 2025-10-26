from django.urls import path
from . import views

app_name = 'contabilidad'  # namespace para usar en templates y reverse()

urlpatterns = [
    path('', views.login_view, name='login'),  # raíz de la app
    path('login/', views.login_view, name='login'),
    path('panel/', views.panel_principal, name='panel_principal_extra'),  # opcional, si quieres acceso directo
    path('catalogo/', views.catalogo_cuentas, name='catalogoCuentas'),  # catálogo de cuentas
    
]
