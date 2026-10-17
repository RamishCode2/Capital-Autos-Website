from django.conf import settings
from django.db import migrations


def create_missing_profiles(apps, schema_editor):
    Profile = apps.get_model("accounts", "Profile")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    database = schema_editor.connection.alias
    for user_id in User.objects.using(database).values_list("pk", flat=True).iterator():
        Profile.objects.using(database).get_or_create(user_id=user_id)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_profile_avatar_url"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_missing_profiles, migrations.RunPython.noop),
    ]
