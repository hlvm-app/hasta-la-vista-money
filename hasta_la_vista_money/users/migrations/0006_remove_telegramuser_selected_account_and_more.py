# Generated by Django 4.2.2 on 2023-06-19 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_telegramuser_selected_account_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='selected_account',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='selected_account_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]