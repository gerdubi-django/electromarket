from django.db import migrations


def create_default_admin(apps, schema_editor):
    user_model = apps.get_model("auth", "User")
    admin_user, created = user_model.objects.get_or_create(
        username="admin",
        defaults={
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
            "email": "admin@electromarket.local",
        },
    )
    if created or not admin_user.check_password("12345"):
        admin_user.set_password("12345")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save(update_fields=["password", "is_staff", "is_superuser", "is_active"])


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_default_admin, migrations.RunPython.noop),
    ]
