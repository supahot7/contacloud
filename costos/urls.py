from django.urls import path
from . import views

app_name = 'costos'

urlpatterns = [
    
    path('manoObra/', views.mano_obra, name='manoObra'),
    path('manoObra/eliminar/<int:id>/', views.eliminar_mano_obra, name='eliminar_mano_obra'),
    path('costos-indirectos/', views.costos_indirectos, name='costosIndirectos'),
    path('costos-indirectos/eliminar/<int:id>/', views.eliminar_costo_indirecto, name='eliminar_costo_indirecto'),
    path('planilla/', views.planilla, name='planilla'),
    path('planilla/eliminar/<int:id>/', views.eliminar_registro_planilla, name='eliminar_registro_planilla'),
    path('planilla/calcular-ajax/', views.calcular_planilla_ajax, name='calcular_planilla_ajax'),
]
   