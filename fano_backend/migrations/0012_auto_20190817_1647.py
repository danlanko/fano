# Generated by Django 2.2.3 on 2019-08-17 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fano_backend', '0011_auto_20190817_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='post',
            new_name='image',
        ),
    ]