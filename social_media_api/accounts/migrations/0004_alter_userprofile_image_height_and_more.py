# Generated by Django 5.1.4 on 2025-01-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_image_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image_height',
            field=models.PositiveIntegerField(blank=True, default=60, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image_width',
            field=models.PositiveIntegerField(blank=True, default=60, null=True),
        ),
    ]
