# Generated by Django 5.1.1 on 2024-10-25 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='PersonaFoM',
            field=models.CharField(default='Pf', max_length=10),
        ),
        migrations.AddField(
            model_name='borrower',
            name='exteriorNumber',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='borrower',
            name='municipality',
            field=models.CharField(default='Muni', max_length=50),
        ),
        migrations.AddField(
            model_name='borrower',
            name='nationality',
            field=models.CharField(default='MX', max_length=50),
        ),
    ]