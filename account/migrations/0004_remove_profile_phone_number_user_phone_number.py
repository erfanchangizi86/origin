# Generated by Django 5.0.7 on 2024-07-31 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=1, max_length=11),
            preserve_default=False,
        ),
    ]
