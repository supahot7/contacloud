from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.login_view, name='login'),  # Ruta raíz va al login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]