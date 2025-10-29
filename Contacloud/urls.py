from django.contrib import admin
from django.urls import path, include
from usuarios.views import dashboard_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contabilidad.urls')),  # Todas las URLs de contabilidad
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
