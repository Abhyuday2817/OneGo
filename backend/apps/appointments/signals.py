# apps/appointments/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Appointment


@receiver(post_save, sender=Appointment)
def update_mentor_availability(sender, instance, created, **kwargs):
    """
    Automatically update mentor availability after appointment is saved.
    Marks mentor as unavailable if a confirmed appointment is created.
    """
    if instance.status == 'confirmed':
        instance.mentor.available = False
        instance.mentor.save(update_fields=["available"])


@receiver(post_delete, sender=Appointment)
def restore_mentor_availability(sender, instance, **kwargs):
    """
    Restore mentor availability when an appointment is deleted.
    Example: Student cancels or admin deletes the session.
    """
    instance.mentor.available = True
    instance.mentor.save(update_fields=["available"])
