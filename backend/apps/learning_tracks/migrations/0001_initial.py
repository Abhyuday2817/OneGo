# Generated by Django 5.2.3 on 2025-07-02 12:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("courses", "0010_alter_course_schedule_info"),
        ("mentors", "0007_mentorprofile_availability_slots_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningTrack",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "courses",
                    models.ManyToManyField(
                        related_name="learning_tracks", to="courses.course"
                    ),
                ),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="learning_tracks",
                        to="mentors.mentorprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TrackEnrollment",
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
                (
                    "progress",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("is_completed", models.BooleanField(default=False)),
                ("enrolled_at", models.DateTimeField(auto_now_add=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="learning_tracks.learningtrack",
                    ),
                ),
            ],
            options={
                "unique_together": {("track", "student")},
            },
        ),
    ]
