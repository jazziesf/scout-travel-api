# Generated by Django 2.1.5 on 2019-01-11 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190111_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
