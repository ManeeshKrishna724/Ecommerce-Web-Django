# Generated by Django 4.2 on 2023-05-25 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_product_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='owner',
        ),
    ]
