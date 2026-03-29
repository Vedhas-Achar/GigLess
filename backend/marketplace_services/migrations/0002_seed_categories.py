from django.db import migrations


def seed_categories(apps, schema_editor):
    category_model = apps.get_model('marketplace_services', 'Category')
    defaults = [
        'Programming',
        'Graphic Design',
        'Writing',
        'Tutoring',
        'Resume Writing',
    ]
    for name in defaults:
        category_model.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('marketplace_services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
