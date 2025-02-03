

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0012_city_pincode_delete_deliveryzone_alter_order_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.ImageField(default='image.jpg', upload_to='media/products/'),
        ),
    ]
