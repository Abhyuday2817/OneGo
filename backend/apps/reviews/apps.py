from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reviews'
    label = 'mentor_reviews'
    def ready(self):
        import apps.reviews.signals  # ✅ full dotted path
