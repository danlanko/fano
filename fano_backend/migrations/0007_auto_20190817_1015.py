# Generated by Django 2.2.3 on 2019-08-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fano_backend', '0006_member_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='about_me',
            field=models.TextField(default='Crazy Ass Fuck', help_text='Describe yourself in 300 words or less'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='profession',
            field=models.CharField(default='Artist', max_length=200),
            preserve_default=False,
        ),
    ]
