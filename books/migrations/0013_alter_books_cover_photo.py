# Generated by Django 3.2.12 on 2022-04-13 06:02

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_applications_confirm_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='books/%Y/%M'),
        ),
    ]
