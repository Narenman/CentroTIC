# Generated by Django 2.1.7 on 2019-08-07 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Humedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_humedad', models.FloatField()),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='LecturaTAGSRFID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('tag_leido', models.CharField(max_length=50)),
                ('id_tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sensores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sensor', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tarjetas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tarjeta', models.CharField(max_length=50)),
                ('ubicacion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Temperatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_temperatura', models.FloatField()),
                ('fecha', models.DateTimeField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_sensado.Sensores')),
            ],
        ),
        migrations.AddField(
            model_name='sensores',
            name='tarjeta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_sensado.Tarjetas'),
        ),
        migrations.AddField(
            model_name='lecturatagsrfid',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_sensado.Sensores'),
        ),
        migrations.AddField(
            model_name='humedad',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_sensado.Sensores'),
        ),
        migrations.AddField(
            model_name='gases',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_sensado.Sensores'),
        ),
    ]
