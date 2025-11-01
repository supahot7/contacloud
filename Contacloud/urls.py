from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='root_login'),  # Ruta raíz directa a la vista
    path('login/', include('usuarios.urls')),
    path('contabilidad/', include('contabilidad.urls')),
    path('logout/', include('usuarios.urls')),
]