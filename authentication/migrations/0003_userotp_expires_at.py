# Generated by Django 5.1.6 on 2025-03-04 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_userotp_is_verified_alter_userotp_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userotp',
            name='expires_at',
            field=models.DateTimeField(null=True),
        ),
    ]
