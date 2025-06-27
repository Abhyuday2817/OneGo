from django.db import models

class MentorProfileQuerySet(models.QuerySet):
    def top_rated(self, min_rating=4.0):
        return self.filter(rating__gte=min_rating).order_by("-rating", "-num_reviews")
