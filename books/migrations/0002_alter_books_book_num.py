# Generated by Django 3.2.12 on 2022-02-04 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='book_num',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
