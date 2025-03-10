# Generated by Django 5.0.8 on 2024-08-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_card_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('VISA', 'Visa'), ('MASTERCARD', 'Mastercard'), ('DISCOVER', 'Discover'), ('AMEX', 'Amex')], max_length=20),
        ),
        migrations.AlterField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
