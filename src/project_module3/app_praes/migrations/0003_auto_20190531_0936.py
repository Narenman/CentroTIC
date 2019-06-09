# Generated by Django 2.1.7 on 2019-05-31 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_praes', '0002_kitnariz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asociacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asociacion', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='kitnariz',
            name='asociacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app_praes.Asociacion'),
            preserve_default=False,
        ),
    ]