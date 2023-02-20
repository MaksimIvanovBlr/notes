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
    datestart = models.DateField(
        verbose_name='Дата начала абонемента', 
        auto_now_add=True)

    status = models.BooleanField(
        verbose_name='Активный'
    )

    quantity = models.SmallIntegerField(
        verbose_name='Количество занятий',
        
    )