# Generated by Django 5.2.3 on 2025-06-27 18:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Programming", "Programming"),
                            ("Design", "Design"),
                            ("Marketing", "Marketing"),
                            ("Music", "Music"),
                            ("Language", "Language"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("budget_min", models.DecimalField(decimal_places=2, max_digits=10)),
                ("budget_max", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "preferred_language",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "timeline_days",
                    models.PositiveIntegerField(
                        help_text="Preferred completion time in days"
                    ),
                ),
                ("is_open", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="learning_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LearningRequestProposal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("proposal_text", models.TextField()),
                (
                    "proposed_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("estimated_days", models.PositiveIntegerField()),
                ("is_selected", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="proposals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="proposals",
                        to="learning_requests.learningrequest",
                    ),
                ),
            ],
            options={
                "unique_together": {("mentor", "request")},
            },
        ),
    ]
