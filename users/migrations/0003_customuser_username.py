# Generated by Django 5.0.8 on 2024-08-13 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_options_remove_customuser_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
    ]
