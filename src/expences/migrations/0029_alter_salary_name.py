# Generated by Django 4.1.2 on 2023-02-24 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expences", "0028_alter_perday_salary_method"),
    ]

    operations = [
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
