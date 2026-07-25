from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("products", "0004_product_slug")]

    operations = [
        migrations.AddField(model_name="product", name="average_rating", field=models.DecimalField(decimal_places=1, default=0, help_text="Optional product rating from 0.0 to 5.0.", max_digits=2)),
        migrations.AddField(model_name="product", name="badge_label", field=models.CharField(blank=True, help_text="Optional card badge, for example: Hot, New, or Best Seller.", max_length=30)),
        migrations.AddField(model_name="product", name="homepage_order", field=models.PositiveIntegerField(default=0, help_text="Lower numbers appear first in homepage sections.")),
        migrations.AddField(model_name="product", name="is_best_seller", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="product", name="is_featured", field=models.BooleanField(default=False, help_text="Show this product in Recommended For You.")),
        migrations.AddField(model_name="product", name="is_flash_sale", field=models.BooleanField(default=False, help_text="Show this product in the homepage Flash Sales section.")),
        migrations.AddField(model_name="product", name="is_new", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="product", name="review_count", field=models.PositiveIntegerField(default=0)),
    ]
