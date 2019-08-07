# Generated by Django 2.1.7 on 2019-08-07 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_praes', '0020_auto_20190806_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ubicacion_lectura',
            options={'managed': True, 'ordering': ['etiqueta_ubicacion'], 'verbose_name': 'Ubicacion_lectura', 'verbose_name_plural': 'Ubicacion_lecturas'},
        ),
        migrations.AlterField(
            model_name='ciudad',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paws.Departamento'),
        ),
        migrations.DeleteModel(
            name='Departamento',
        ),
    ]