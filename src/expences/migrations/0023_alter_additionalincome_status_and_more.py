# Generated by Django 4.1.2 on 2023-02-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expences", "0022_expediture_reserv_value_of_days_exp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="additionalincome",
            name="status",
            field=models.BooleanField(default=True, verbose_name="Использован"),
        ),
        migrations.AlterField(
            model_name="perday",
            name="salary_method",
            field=models.CharField(
                choices=[
                    (
                        "Расчет по факту зачисления",
                        "Расчет по мере зачисления на карту",
                    ),
                    ("Расчет за полный месяц", "Расчет за полный месяц"),
                ],
                default="Расчет за полный месяц",
                max_length=50,
                verbose_name="Способ расчета",
            ),
        ),
    ]
