# Generated by Django 2.1.7 on 2019-06-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_praes', '0003_auto_20190531_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anemometro',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='materialparticulado',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='no2',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='polvo',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='so2',
            name='sensor',
        ),
        migrations.AlterField(
            model_name='ch4',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='co',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='co2',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='humedad',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='luzuv',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='materialorganico',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='metanopropanoco',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='o3',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='presionatmosferica',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='temperatura',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Anemometro',
        ),
        migrations.DeleteModel(
            name='MaterialParticulado',
        ),
        migrations.DeleteModel(
            name='NO2',
        ),
        migrations.DeleteModel(
            name='Polvo',
        ),
        migrations.DeleteModel(
            name='SO2',
        ),
    ]
