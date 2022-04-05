# Generated by Django 3.2.12 on 2022-03-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20220329_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='loanedbooks',
            name='point',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]