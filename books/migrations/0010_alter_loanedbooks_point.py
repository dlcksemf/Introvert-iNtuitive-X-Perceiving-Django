# Generated by Django 3.2.12 on 2022-03-29 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20220329_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanedbooks',
            name='point',
            field=models.IntegerField(default=0),
        ),
    ]
