# Generated by Django 3.2.5 on 2022-06-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20220624_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='session_key',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]