# Generated by Django 3.2.12 on 2022-04-07 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_alter_loanedgame_return_due_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_amount',
            field=models.IntegerField(default=1),
        ),
    ]
