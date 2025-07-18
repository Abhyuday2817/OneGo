# Generated by Django 5.2.3 on 2025-06-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mentors", "0003_mentorprofile_expertise"),
    ]

    operations = [
        migrations.AddField(
            model_name="mentorprofile",
            name="linkedin_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="mentorprofile",
            name="youtube_url",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="mentorprofile",
            name="languages",
            field=models.CharField(
                blank=True,
                help_text="Comma-separated ISO language codes (e.g. en, hi, fr)",
                max_length=200,
            ),
        ),
    ]
