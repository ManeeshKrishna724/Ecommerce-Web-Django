# Generated by Django 4.2 on 2023-05-20 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_address_landmark'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='town_city',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
