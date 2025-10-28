from django.urls import path
from . import views

app_name = 'contabilidad'  # namespace para usar en templates y reverse()

urlpatterns = [
    path('', views.login_view, name='login'),  # raíz de la app
    path('login/', views.login_view, name='login'),
    path('panel/', views.panel_principal, name='panel_principal_extra'),  # opcional, si quieres acceso directo
    path('catalogo/', views.catalogo_cuentas, name='catalogo_cuentas'),  # catálogo de cuentas
    path('transacciones/', views.nueva_transaccion, name='nueva_transaccion'), # nueva transaccion
    path('estados/', views.estado_financiero, name='estado_financiero'),  # Estados financieros
    path('libro_mayor/', views.libro_mayor, name='libro_mayor'),  # Estados financieros
     path('libro-mayor/imprimir/', views.libro_mayor_imprimir, name='libro_mayor_imprimir'),
    
]
