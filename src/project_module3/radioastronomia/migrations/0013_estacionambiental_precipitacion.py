# Generated by Django 2.1.7 on 2019-09-18 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioastronomia', '0012_auto_20190918_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='estacionambiental',
            name='precipitacion',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]