# Generated by Django 3.2.12 on 2022-04-07 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_game_game_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='play_time',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
