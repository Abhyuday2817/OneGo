# Generated by Django 5.2.3 on 2025-06-21 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mentor_reviews", "0001_initial"),
        ("mentors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="reviewee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_reviews",
                to="mentors.mentorprofile",
            ),
        ),
    ]
