from django.apps import AppConfig

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.payments'
    label = 'mentor_payments'
    def ready(self):
        # import any signal handlers here
        pass
