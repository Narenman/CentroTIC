# Generated by Django 2.1.7 on 2019-09-27 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioastronomia', '0017_auto_20190927_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estadocamara',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camara', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Estadocamara',
                'verbose_name_plural': 'Estadocamaras',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Estadoestacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estacion', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Estadoestacion',
                'verbose_name_plural': 'Estadoestacions',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
