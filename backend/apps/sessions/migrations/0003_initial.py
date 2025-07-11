# Generated by Django 5.2.3 on 2025-06-21 14:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("mentoring_sessions", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions_as_student",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddIndex(
            model_name="session",
            index=models.Index(
                fields=["mentor", "start_time"], name="mentoring_s_mentor__d0b417_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="session",
            index=models.Index(
                fields=["student", "start_time"], name="mentoring_s_student_733130_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="session",
            unique_together={("mentor", "start_time", "end_time")},
        ),
    ]
