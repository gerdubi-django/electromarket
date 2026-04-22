from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_default_admin(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    user_model = apps.get_model(app_label, model_name)

    user_model.objects.update_or_create(
        username="admin",
        defaults={
            "email": "admin@electromarket.local",
            "password": make_password("12345"),
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_default_admin, migrations.RunPython.noop),
    ]
