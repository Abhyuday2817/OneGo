# apps/appointments/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Appointment


@receiver(post_save, sender=Appointment)
def update_mentor_availability(sender, instance, created, **kwargs):
    """
    Update mentor availability after an appointment is saved.
    Example: Mark as unavailable if status is 'confirmed'.
    """
    if instance.status == 'confirmed':
        instance.mentor.available = False
        instance.mentor.save()


@receiver(post_delete, sender=Appointment)
def restore_mentor_availability(sender, instance, **kwargs):
    """
    Restore mentor availability when an appointment is deleted.
    """
    instance.mentor.available = True
    instance.mentor.save()
