# Generated by Django 4.2.11 on 2024-04-08 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("authtoken", "0005_alter_token_user"),
        ("budget", "0005_alter_datelist_user_alter_planning_user"),
        ("admin", "0004_alter_logentry_user"),
        ("loan", "0021_alter_loan_user_alter_paymentmakeloan_user_and_more"),
        ("expense", "0020_alter_expense_user_alter_expensecategory_user"),
        ("income", "0023_alter_income_user_alter_incomecategory_user"),
        ("receipts", "0014_alter_customer_user_alter_product_user_and_more"),
        ("account", "0027_alter_account_user_alter_transfermoneylog_user"),
        ("users", "0011_selectedaccount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="telegramuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="telegram_users",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
