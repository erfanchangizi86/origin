# Generated by Django 5.0.7 on 2024-08-31 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_category_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_deleted',
        ),
    ]
