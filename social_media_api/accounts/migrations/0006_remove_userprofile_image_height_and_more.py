# Generated by Django 5.1.4 on 2025-01-05 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image_height',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='image_width',
        ),
    ]
