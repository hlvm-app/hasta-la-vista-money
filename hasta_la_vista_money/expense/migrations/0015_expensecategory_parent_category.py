# Generated by Django 4.2.7 on 2023-11-15 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("expense", "0014_rename_category_expensecategory_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="expensecategory",
            name="parent_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subcategories",
                to="expense.expensecategory",
            ),
        ),
    ]