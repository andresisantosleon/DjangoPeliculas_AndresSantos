# Generated by Django 3.2.7 on 2021-09-18 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VotacionPeliculas', '0002_peliculas_imdbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peliculas',
            name='votos',
            field=models.IntegerField(default=0),
        ),
    ]