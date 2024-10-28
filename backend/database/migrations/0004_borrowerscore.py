# Generated by Django 5.1.1 on 2024-10-28 02:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_alter_credithistory_date_account_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowerScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('val_score', models.IntegerField()),
                ('code_score', models.FloatField()),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BorrowerScore', to='database.borrower')),
            ],
        ),
    ]
