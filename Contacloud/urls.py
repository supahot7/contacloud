


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contabilidad.urls')),  # Todas las URLs de contabilidad
]
