from django.urls import path
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('panel/', views.panel_principal, name='panel_principal'),
    path('catalogo/', views.catalogo_cuentas, name='catalogo_cuentas'),
    path('cuenta/<int:pk>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('nueva-transaccion/', views.nueva_transaccion, name='nueva_transaccion'),
    path('guardar-transaccion/', views.guardar_transaccion, name='guardar_transaccion'),
    path('libro-mayor/', views.libro_mayor, name='libro_mayor'),
    path('asiento/<int:asiento_id>/', views.detalle_asiento, name='detalle_asiento'),
    path('estados/', views.estados_financieros, name='estadosFinancieros'), # Estados Financieros
    path('balance/', views.balance_general, name='balanceGeneral'), # Balance General
    path('estado/', views.estado_resultados, name='estadoResultados'), # Estado de Resultados
    path('estadoCapital/', views.estado_capital, name='estadoCapital'), # Estado de Capital
    path('inventario/', views.inventario_licencias, name='inventarioLicencias'), # Inventario de Licencias
    path('planilla/', views.planilla, name='planilla'), # Cálculo de Planilla
    path('api/cuentas/', views.api_cuentas, name='api_cuentas'),
    path('api/cuentas/<int:cuenta_id>/', views.api_cuenta_detalle, name='api_cuenta_detalle'),
    path('api/licencias/', views.api_licencias, name='api_licencias'),
    path('api/licencias/<int:licencia_id>/agregar-stock/', views.api_licencia_agregar_stock, name='api_licencia_agregar_stock'),
    path('api/licencias/<int:licencia_id>/', views.api_licencia_detalle, name='api_licencia_detalle'),
    path('api/licencias/dashboard/', views.api_licencias_dashboard, name='api_licencias_dashboard'),
   
]
   
