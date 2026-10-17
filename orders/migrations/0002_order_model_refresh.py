from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


def populate_order_numbers(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    for order in Order.objects.all():
        order.order_number = f"ORD-{order.pk:05d}"
        order.save(update_fields=["order_number"])


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="order_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.RunPython(populate_order_numbers, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="order",
            name="order_number",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name="order",
            name="postal_code",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AddField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RenameField(
            model_name="order",
            old_name="total",
            new_name="total_price",
        ),
        migrations.AlterField(
            model_name="order",
            name="full_name",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="order",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("COD", "Cash On Delivery"),
                    ("CARD", "Card"),
                    ("JAZZCASH", "JazzCash"),
                    ("EASYPAISA", "EasyPaisa"),
                    ("PAYONEER", "Payoneer"),
                ],
                default="COD",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Confirmed", "Confirmed"),
                    ("Processing", "Processing"),
                    ("Shipped", "Shipped"),
                    ("Out For Delivery", "Out For Delivery"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                    ("Refunded", "Refunded"),
                ],
                default="Pending",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
