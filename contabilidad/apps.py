from django.apps import AppConfig

class ContabilidadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contabilidad'
    
    def ready(self):
        # Esta línea debe estar presente
        import contabilidad.signals
        print("✅ Señales de contabilidad registradas")  