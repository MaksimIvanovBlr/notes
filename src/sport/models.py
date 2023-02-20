from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class SubscriptionModel(models.Model):
    X = 'Безлимитный'
    Y = ' На количество занятий'

    CHOISE_GROUP = {
        (X, 'Расчет за полный месяц'),
        (Y, 'Расчет по мере зачисления на карту'),
    }

    user = models.ForeignKey(
        user,
        verbose_name='Пользователь',
        related_name='user_subscription',
        on_delete=models.PROTECT
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50)

    datestart = models.DateField(
        verbose_name='Дата начала абонемента', 
        auto_now_add=True)

    status = models.BooleanField(
        verbose_name='Активный'
    )

    quantity = models.SmallIntegerField(
        verbose_name='Количество занятий',

    )


class SubscriptionVisit(models.Model):
    user = models.ForeignKey(
        user,
        verbose_name='Пользователь',
        related_name='user_subscription_visits',
        on_delete=models.PROTECT
    )
    subscription = models.ForeignKey(
        'sport.SubscriptionModel',
        verbose_name='Абонемент',
        related_name='subscription_subscription_visits',
        on_delete=models.PROTECT
    )
    visit_date = models.DateTimeField(
        verbose_name='Дата посещения',
        auto_now_add=True,

    )