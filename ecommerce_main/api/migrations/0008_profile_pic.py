# Generated by Django 4.2 on 2023-05-15 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_product_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pic',
            field=models.CharField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', max_length=500),
        ),
    ]
