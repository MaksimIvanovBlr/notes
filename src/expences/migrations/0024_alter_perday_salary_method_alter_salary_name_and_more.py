# Generated by Django 4.1.2 on 2023-02-16 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("expences", "0023_alter_additionalincome_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="perday",
            name="salary_method",
            field=models.CharField(
                choices=[
                    ("Расчет за полный месяц", "Расчет за полный месяц"),
                    (
                        "Расчет по факту зачисления",
                        "Расчет по мере зачисления на карту",
                    ),
                ],
                default="Расчет за полный месяц",
                max_length=50,
                verbose_name="Способ расчета",
            ),
        ),
        migrations.AlterField(
            model_name="salary",
            name="name",
            field=models.CharField(
                choices=[("зарплата", "зарплата"), ("аванс", "аванс")],
                default="зарплата",
                max_length=50,
                verbose_name="Наименование",
            ),
        ),
        migrations.CreateModel(
            name="DailyConsumption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "per_month",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=100,
                        verbose_name="Месячный остаток",
                    ),
                ),
                (
                    "buffer_money",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=100,
                        verbose_name="Дневной остаток",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_daily_cons",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
        ),
    ]