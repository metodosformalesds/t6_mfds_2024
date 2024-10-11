# Generated by Django 5.1.1 on 2024-10-11 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreditHistory',
            fields=[
                ('id_check', models.AutoField(primary_key=True, serialize=False)),
                ('date_account_open', models.DateField()),
                ('actual_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lim_credit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_history', models.CharField(max_length=50)),
                ('current_pay_status', models.CharField(max_length=10)),
                ('accounts_open', models.IntegerField()),
                ('accounts_closed', models.IntegerField()),
                ('account_fixed_payment', models.BooleanField()),
                ('num_mop1', models.IntegerField()),
                ('num_mop2', models.IntegerField()),
                ('num_mop3', models.IntegerField()),
                ('num_mop4', models.IntegerField()),
                ('num_mop5', models.IntegerField()),
                ('num_mop6', models.IntegerField()),
                ('num_mop7', models.IntegerField()),
                ('check_date', models.DateField()),
                ('code_score', models.FloatField()),
                ('place_of_work', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]