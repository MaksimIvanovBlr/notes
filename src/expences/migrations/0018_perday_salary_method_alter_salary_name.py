# Generated by Django 4.1.2 on 2023-01-10 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expences', '0017_perday_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='perday',
            name='salary_method',
            field=models.BooleanField(blank=True, null=True, verbose_name='Расчет за полный месяц'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='name',
            field=models.CharField(choices=[('аванс', 'аванс'), ('зарплата', 'зарплата')], default='зарплата', max_length=50, verbose_name='Наименование'),
        ),
    ]
