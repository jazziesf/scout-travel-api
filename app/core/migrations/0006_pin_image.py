# Generated by Django 2.1.5 on 2019-01-09 04:34

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190108_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.pin_image_file_path),
        ),
    ]
