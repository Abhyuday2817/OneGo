from django.db import migrations
from django.utils.text import slugify
import itertools

def populate_slugs(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')

    for course in Course.objects.all():
        if not course.slug:
            base_slug = slugify(course.title or "course")
            slug = base_slug
            for i in itertools.count(1):
                if not Course.objects.filter(slug=slug).exclude(pk=course.pk).exists():
                    break
                slug = f"{base_slug}-{i}"
            course.slug = slug
            course.save()

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs),
    ]
