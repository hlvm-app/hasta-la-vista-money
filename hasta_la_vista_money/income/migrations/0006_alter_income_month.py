# Generated by Django 4.1.7 on 2023-03-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0005_alter_income_amount_alter_income_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='month',
            field=models.CharField(choices=[('Январь 2023', 'Январь 2023'), ('Февраль 2023', 'Февраль 2023'), ('Март 2023', 'Март 2023'), ('Апрель 2023', 'Апрель 2023'), ('Май 2023', 'Май 2023'), ('Июнь 2023', 'Июнь 2023'), ('Июль 2023', 'Июль 2023'), ('Август 2023', 'Август 2023'), ('Сентябрь 2023', 'Сентябрь 2023'), ('Октябрь 2023', 'Октябрь 2023'), ('Ноябрь 2023', 'Ноябрь 2023'), ('Декабрь 2023', 'Декабрь 2023')], max_length=20),
        ),
    ]
