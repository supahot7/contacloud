from django.urls import path
from . import views

app_name = 'contabilidad'  # namespace para usar en templates y reverse()

urlpatterns = [
    path('', views.login_view, name='login'),  # raíz de la app
    path('login/', views.login_view, name='login'),
    path('panel/', views.panel_principal, name='panel_principal_extra'),  # opcional, si quieres acceso directo
    path('catalogo/', views.catalogo_cuentas, name='catalogoCuentas'),  # catálogo de cuentas
    path('estados/', views.estados_financieros, name='estadosFinancieros'), # Estados Financieros
    path('balance/', views.balance_general, name='balanceGeneral'), # Balance General
    path('estado/', views.estado_resultados, name='estadoResultados'), # Estado de Resultados
    path('estadoCapital/', views.estado_capital, name='estadoCapital'), # Estado de Capital
    path('contabilidadCostos/', views.contabilidad_costos, name='contabilidadCostos'), # Contabilidad de Costos
    path('manoObra/', views.mano_obra, name='manoObra'), # Mano de obra
    path('inventario/', views.inventario_licencias, name='inventarioLicencias'), # Inventario de Licencias
]
