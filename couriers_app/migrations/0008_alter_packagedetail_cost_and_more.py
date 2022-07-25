# Generated by Django 4.0.2 on 2022-03-26 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('couriers_app', '0007_packagedetail_pack_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagedetail',
            name='cost',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='packagedetail',
            name='drop_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='packagedetail',
            name='pick_up_depot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='couriers_app.depot'),
        ),
    ]
