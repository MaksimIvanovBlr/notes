from django.db import models
from django.contrib.auth import get_user_model

S_user = get_user_model()


#  данные пользователя(расход на день, дата получения ЗП, способ расчета, реальны баланс карты)
class PerDay(models.Model):

    X = 'Расчет за полный месяц'
    Y = 'Расчет по факту зачисления'

    CHOISE_GROUP = {
        (X, 'Расчет за полный месяц'),
        (Y, 'Расчет по мере зачисления на карту'),
    }
    user = models.OneToOneField(
        S_user,
        verbose_name="Пользователь",
        related_name='user_per_day',
        on_delete=models.CASCADE
    )
    # сумма расхода на день
    value = models.DecimalField(
        verbose_name='Расход на день',
        max_digits=10,
        decimal_places=2
    )
    # поле, которое будет заполняться для рассчета ЗП(день получения зп)
    day = models.DateField(
        verbose_name='День зарплаты'

    )
    # Указания способа расчета. расчет за полный месяц(аванс+ЗП) или по мере поступления денег на карту
    salary_method = models.CharField(
        verbose_name='Способ расчета',
        max_length=50,
        choices=CHOISE_GROUP,
        default=X)

    # реальный баланс карты
    balance = models.DecimalField(
        verbose_name='Реальный баланс карты',
        max_digits=100,
        decimal_places=2,
        default=0
    )



# расходы
class Expediture(models.Model):
    user = models.ForeignKey(
        S_user,
        verbose_name="Пользователь",
        related_name='user_expences',
        on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50)
    value = models.DecimalField(
        verbose_name='Значение',
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField(
        verbose_name='дата изменения',
        auto_now=True
    )
    status = models.BooleanField(
        verbose_name='Оплачено'
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=500,
        blank=True,
        null=True
    )


# аванс/зарплата
class Salary(models.Model):
    X = 'аванс'
    Y = 'зарплата'

    CHOISE_GROUP = {
        (X, 'аванс'),
        (Y, 'зарплата'),
    }

    user = models.ForeignKey(
        S_user,
        verbose_name="Пользователь",
        related_name='user_salary',
        on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50,
        choices=CHOISE_GROUP,
        default=Y)
    value = models.DecimalField(
        verbose_name='Значение',
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField(
        verbose_name='дата изменения',
        auto_now_add=True
    )
    status = models.BooleanField(
        verbose_name='статус',
        default=True
    )


# дополнительные доходы
class AdditionalIncome(models.Model):
    user = models.ForeignKey(
        S_user,
        verbose_name="Пользователь",
        related_name='user_additional_income',
        on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50,
    )
    value = models.DecimalField(
        verbose_name='Значение',
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField(
        verbose_name='дата изменения',
        auto_now_add=True
    )
    status = models.BooleanField(
        verbose_name='Использован',
        default=True
    )


# резерв
class Reserv(models.Model):
    user = models.OneToOneField(
        S_user,
        verbose_name="Пользователь",
        related_name='user_reserv',
        on_delete=models.CASCADE
    )

    value = models.DecimalField(
        verbose_name='Значение',
        max_digits=100,
        decimal_places=2,
        default=0
    )

    date = models.DateField(
        verbose_name='Дата изменения',
        auto_now_add=True
    )


class DailyConsumption(models.Model):
    user = models.OneToOneField(
        S_user,
        verbose_name="Пользователь",
        related_name='user_daily_cons',
        on_delete=models.CASCADE)

    per_month = models.DecimalField(
        verbose_name='Месячный остаток',
        max_digits=100,
        decimal_places=2,
        default=0
    )

    buffer_money = models.DecimalField(
        verbose_name='Дневной остаток',
        max_digits=100,
        decimal_places=2,
        default=0
    )