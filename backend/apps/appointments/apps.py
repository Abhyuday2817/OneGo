# apps/appointments/apps.py

from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appointments'  # Ensure correct full path to the app

    def ready(self):
        # Import signals properly using full path
        import apps.appointments.signals  # noqa
