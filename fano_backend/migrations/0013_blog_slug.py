# Generated by Django 2.2.3 on 2019-08-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fano_backend', '0012_auto_20190817_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(default='slugify_something'),
            preserve_default=False,
        ),
    ]