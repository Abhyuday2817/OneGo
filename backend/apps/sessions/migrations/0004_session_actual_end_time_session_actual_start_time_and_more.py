# Generated by Django 5.2.3 on 2025-06-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mentoring_sessions", "0003_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="actual_end_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="session",
            name="actual_start_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="session",
            name="duration_minutes",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="session",
            name="total_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=8, null=True
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="status",
            field=models.CharField(
                choices=[
                    ("Scheduled", "Scheduled"),
                    ("Ongoing", "Ongoing"),
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Scheduled",
                max_length=20,
            ),
        ),
    ]
