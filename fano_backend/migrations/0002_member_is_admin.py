# Generated by Django 2.2.3 on 2019-08-13 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fano_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]