# Generated by Django 4.0.2 on 2022-03-26 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('couriers_app', '0006_employee_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagedetail',
            name='pack_weight',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
