# Generated by Django 2.1.7 on 2019-07-08 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_praes', '0004_auto_20190627_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ch4',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='co',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='co2',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='luzuv',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='materialorganico',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='metanopropanoco',
            name='sensor',
        ),
        migrations.RemoveField(
            model_name='o3',
            name='sensor',
        ),
        migrations.AddField(
            model_name='kitnariz',
            name='kit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_praes.Sensores'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CH4',
        ),
        migrations.DeleteModel(
            name='CO',
        ),
        migrations.DeleteModel(
            name='CO2',
        ),
        migrations.DeleteModel(
            name='LuzUV',
        ),
        migrations.DeleteModel(
            name='MaterialOrganico',
        ),
        migrations.DeleteModel(
            name='MetanoPropanoCO',
        ),
        migrations.DeleteModel(
            name='O3',
        ),
    ]
