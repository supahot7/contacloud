from django.urls import path
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('panel/', views.panel_principal, name='panel_principal'),
    path('catalogo/', views.catalogo_cuentas, name='catalogo_cuentas'),
    path('cuenta/<int:pk>/', views.detalle_cuenta, name='detalle_cuenta'),
    path('nueva-transaccion/', views.nueva_transaccion, name='nueva_transaccion'),
    path('guardar-transaccion/', views.guardar_transaccion, name='guardar_transaccion'),
    path('libro-diario/', views.libro_diario, name='libro_diario'),
    path('asiento/<int:asiento_id>/', views.detalle_asiento, name='detalle_asiento'),
    path('estados/', views.estados_financieros, name='estadosFinancieros'), # Estados Financieros
    path('balance/', views.balance_general, name='balanceGeneral'), # Balance General
    path('estado/', views.estado_resultados, name='estadoResultados'), # Estado de Resultados
    path('estadoCapital/', views.estado_capital, name='estadoCapital'), # Estado de Capital
    path('manoObra/', views.mano_obra, name='manoObra'), # Mano de obra
    path('inventario/', views.inventario_licencias, name='inventarioLicencias'), # Inventario de Licencias
    path('planilla/', views.planilla, name='planilla'), # Cálculo de Planilla
]
   
