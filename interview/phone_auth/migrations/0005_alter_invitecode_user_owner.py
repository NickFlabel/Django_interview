# Generated by Django 4.2.4 on 2023-08-19 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phone_auth', '0004_alter_phonecode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitecode',
            name='user_owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invite_code', to=settings.AUTH_USER_MODEL),
        ),
    ]
