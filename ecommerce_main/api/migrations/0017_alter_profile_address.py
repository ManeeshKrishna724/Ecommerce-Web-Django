# Generated by Django 4.2 on 2023-05-25 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_address_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.address'),
        ),
    ]
