from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class BidsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bids'
    verbose_name = 'Mentor Bids'

    def ready(self):
        import apps.bids.signals  # Optional: auto-register signals
        logger.info("✅ Bids app loaded and ready.")


