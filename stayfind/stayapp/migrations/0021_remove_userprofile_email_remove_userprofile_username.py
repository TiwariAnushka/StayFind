# Generated by Django 5.0.6 on 2024-09-07 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stayapp', '0020_userprofile_email_userprofile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
