# Generated by Django 3.2.5 on 2022-06-22 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_userprofile_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='session_id',
        ),
    ]