# Generated by Django 2.1.7 on 2019-08-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radioastronomia', '0007_regioncampana_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regioncampana',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='album/regiones'),
        ),
    ]