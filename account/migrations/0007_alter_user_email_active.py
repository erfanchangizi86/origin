# Generated by Django 5.0.7 on 2024-08-01 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_profile_phone_number_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_active',
            field=models.CharField(blank=True, max_length=72, null=True),
        ),
    ]
