# Generated by Django 5.1.1 on 2024-11-11 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activeloan',
            name='payment_by_term',
        ),
    ]