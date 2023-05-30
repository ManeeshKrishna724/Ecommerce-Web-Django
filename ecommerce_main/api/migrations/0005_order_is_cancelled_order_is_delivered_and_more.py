# Generated by Django 4.2.1 on 2023-05-14 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_product_seller_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_cancelled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_delivered',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='my_orders',
            field=models.ManyToManyField(to='api.order'),
        ),
    ]