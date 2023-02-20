# Generated by Django 4.1.2 on 2023-02-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expences", "0024_alter_perday_salary_method_alter_salary_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reserv",
            name="value_of_days_exp",
        ),
        migrations.AlterField(
            model_name="salary",
            name="name",
            field=models.CharField(
                choices=[("аванс", "аванс"), ("зарплата", "зарплата")],
                default="зарплата",
                max_length=50,
                verbose_name="Наименование",
            ),
        ),
    ]
