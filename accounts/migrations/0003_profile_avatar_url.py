from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_profile_delete_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="avatar_url",
            field=models.URLField(blank=True),
        ),
    ]
