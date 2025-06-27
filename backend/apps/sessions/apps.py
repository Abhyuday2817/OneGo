# apps/sessions/apps.py

from django.apps import AppConfig

class CustomSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sessions'
    label = 'mentoring_sessions'  # ✅ custom unique label
