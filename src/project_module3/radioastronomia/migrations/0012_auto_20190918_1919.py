# Generated by Django 2.1.7 on 2019-09-18 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioastronomia', '0011_bandas_servicios'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estacionambiental',
            old_name='intensidad_luz',
            new_name='radiacion_solar',
        ),
        migrations.RenameField(
            model_name='estacionambiental',
            old_name='luz_uv',
            new_name='vel_viento',
        ),
        migrations.AddField(
            model_name='estacionambiental',
            name='dir_viento',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
