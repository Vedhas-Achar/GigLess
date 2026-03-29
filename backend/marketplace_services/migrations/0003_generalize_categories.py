from django.db import migrations


BROAD_CATEGORIES = [
    'Development / Programming',
    'Tutoring / Education',
    'Art & Design',
    'Music & Dance',
    'Writing & Content',
    'Tech Support',
    'Photography / Media',
    'Other',
]


LEGACY_TO_BROAD = {
    'Programming': 'Development / Programming',
    'Development': 'Development / Programming',
    'Tutoring': 'Tutoring / Education',
    'Graphic Design': 'Art & Design',
    'Writing': 'Writing & Content',
    'Resume Writing': 'Writing & Content',
}


def forward_generalize_categories(apps, schema_editor):
    category_model = apps.get_model('marketplace_services', 'Category')
    service_model = apps.get_model('marketplace_services', 'Service')

    broad_lookup = {}
    for name in BROAD_CATEGORIES:
        category, _ = category_model.objects.get_or_create(name=name)
        broad_lookup[name] = category

    legacy_categories = category_model.objects.exclude(name__in=BROAD_CATEGORIES)
    for legacy in legacy_categories:
        broad_name = LEGACY_TO_BROAD.get(legacy.name, 'Other')
        broad_category = broad_lookup[broad_name]

        service_model.objects.filter(category_id=legacy.id).update(category_id=broad_category.id)
        if not service_model.objects.filter(category_id=legacy.id).exists():
            legacy.delete()


def backward_noop(apps, schema_editor):
    # Category simplification is intentionally one-way for data safety.
    return


class Migration(migrations.Migration):
    dependencies = [
        ('marketplace_services', '0002_seed_categories'),
    ]

    operations = [
        migrations.RunPython(forward_generalize_categories, backward_noop),
    ]
