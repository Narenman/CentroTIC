# Generated by Django 2.1.7 on 2019-10-30 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioastronomia', '0019_auto_20191030_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caracteristicasantena',
            name='perdidas_vector',
        ),
        migrations.RemoveField(
            model_name='caracteristicasantena',
            name='vswr_vector',
        ),
        migrations.AddField(
            model_name='caracteristicasantena',
            name='caracterizacion_csv',
            field=models.FileField(default='', upload_to='caracterizacion'),
            preserve_default=False,
        ),
    ]
