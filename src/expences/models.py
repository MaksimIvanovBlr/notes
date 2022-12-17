from django.db import models
from django.contrib.auth import get_user_model


S_user = get_user_model()

class IncomeAndExpediture(models.Model):
    user = models.ForeignKey(
        S_user,
        verbose_name="Пользователь", 
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
        verbose_name='статус'
        )