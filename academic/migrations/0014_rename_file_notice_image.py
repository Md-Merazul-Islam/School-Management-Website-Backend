# Generated by Django 4.2.15 on 2024-11-19 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0013_alter_notice_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notice',
            old_name='file',
            new_name='image',
        ),
    ]
