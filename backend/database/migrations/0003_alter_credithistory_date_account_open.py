# Generated by Django 5.1.1 on 2024-10-28 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_credithistory_val_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credithistory',
            name='date_account_open',
            field=models.DateField(blank=True, null=True),
        ),
    ]
