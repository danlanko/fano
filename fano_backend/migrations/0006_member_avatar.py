# Generated by Django 2.2.3 on 2019-08-17 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fano_backend', '0005_auto_20190817_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar'),
        ),
    ]
