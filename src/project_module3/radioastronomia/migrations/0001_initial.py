# Generated by Django 2.1.7 on 2019-08-07 18:17

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumImagenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.FileField(max_length=200, null=True, upload_to='videos/', verbose_name='')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'AlbumImagenes',
                'db_table': '',
                'verbose_name_plural': 'AlbumImageness',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CaracteristicasAntena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_x', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
                ('area_efec', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
                ('directividad_antena', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
                ('referencia', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'CaracteristicasAntena',
                'db_table': '',
                'verbose_name_plural': 'CaracteristicasAntenas',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CaracteristicasEspectro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_v', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
                ('min_v', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
                ('energia', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
            ],
            options={
                'verbose_name': 'CaracteristicasEspectro',
                'db_table': '',
                'verbose_name_plural': 'CaracteristicasEspectros',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CaracteristicasEstacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor', models.CharField(max_length=50)),
                ('variable', models.CharField(max_length=50)),
                ('rango', models.CharField(max_length=50)),
                ('resolucion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'CaracteristicasEstacion',
                'db_table': '',
                'verbose_name_plural': 'CaracteristicasEstacions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Espectro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('espectro', django.contrib.postgres.fields.jsonb.JSONField(encoder='')),
                ('frec_muestreo', models.IntegerField()),
                ('nfft', models.IntegerField()),
                ('frec_central', models.FloatField()),
                ('duracion', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='EstacionAmbiental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('temperatura', models.FloatField()),
                ('humedad_relativa', models.FloatField()),
                ('presion_atomosferica', models.FloatField()),
                ('intensidad_luz', models.FloatField()),
                ('luz_uv', models.FloatField()),
            ],
            options={
                'verbose_name': 'EstacionAmbiental',
                'db_table': '',
                'verbose_name_plural': 'EstacionAmbientals',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=False)),
                ('frecuencia', models.FloatField()),
            ],
            options={
                'verbose_name': 'Estado',
                'db_table': '',
                'verbose_name_plural': 'Estados',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PosicionAntena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('azimut', models.FloatField()),
                ('elevacion', models.FloatField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('antena', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radioastronomia.CaracteristicasAntena')),
            ],
        ),
        migrations.CreateModel(
            name='RegionCampana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=50)),
                ('municipio', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'RegionCampana',
                'db_table': '',
                'verbose_name_plural': 'RegionCampanas',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='posicionantena',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radioastronomia.RegionCampana'),
        ),
        migrations.AddField(
            model_name='estacionambiental',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radioastronomia.RegionCampana'),
        ),
        migrations.AddField(
            model_name='espectro',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radioastronomia.RegionCampana'),
        ),
        migrations.AddField(
            model_name='caracteristicasespectro',
            name='espectro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radioastronomia.Espectro'),
        ),
        migrations.AddField(
            model_name='albumimagenes',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radioastronomia.RegionCampana'),
        ),
    ]
