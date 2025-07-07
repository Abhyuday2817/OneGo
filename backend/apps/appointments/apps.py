# apps/appointments/apps.py

from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appointments'
    verbose_name = "Appointments & Bookings"

    def ready(self):
        """
        Called when the app is fully loaded.
        Used to connect signals and perform setup tasks.
        """
        import apps.appointments.signals  # noqa: F401
