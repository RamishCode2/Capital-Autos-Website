from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HeroSlide",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("eyebrow", models.CharField(blank=True, max_length=80)),
                ("title", models.CharField(max_length=150)),
                ("description", models.CharField(blank=True, max_length=220)),
                ("button_label", models.CharField(default="Shop Now", max_length=40)),
                ("button_url", models.CharField(default="/products/shop/", max_length=255)),
                ("background_image", models.ImageField(blank=True, null=True, upload_to="hero_slides/")),
                ("is_active", models.BooleanField(default=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ("display_order", "id")},
        ),
    ]
