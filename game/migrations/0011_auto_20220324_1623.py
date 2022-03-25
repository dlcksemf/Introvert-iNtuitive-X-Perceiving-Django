# Generated by Django 3.2.12 on 2022-03-24 07:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20220323_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanedgame',
            name='return_due_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 24, 7, 23, 57, 270561, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='loanedgame',
            name='returned_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 24, 7, 23, 57, 270561, tzinfo=utc), null=True),
        ),
    ]
