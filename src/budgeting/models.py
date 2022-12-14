from django.db import models

class Expenses(models.Model):


    flat = models.DecimalField(
        verbose_name='квартира',
        max_digits=5,
        decimal_places=2
    )
    
    utility_costs = models.DecimalField(
        verbose_name='коммуналка',
        max_digits=5,
        decimal_places=2
    )
    
    phone = models.DecimalField(
        verbose_name='телефон',
        max_digits=5,
        decimal_places=2
    )
    
    internet = models.DecimalField(
        verbose_name='интернет',
        max_digits=5,
        decimal_places=2
    )
    
    transport = models.DecimalField(
        verbose_name='транспорт',
        max_digits=5,
        decimal_places=2
    )

    per_day = models.DecimalField(
        verbose_name='за день',
        max_digits=8,
        decimal_places=2
    )

    
class Advance(models.Model):
    income = models.DecimalField(
        verbose_name='аванс',
        max_digits=8,
        decimal_places=2
    )
    date = models.DateField(
        verbose_name='дата поступелния',
        auto_now=True
    )


class Salary(models.Model):
    income = models.DecimalField(
        verbose_name='ЗП',
        max_digits=8,
        decimal_places=2
    )
    date = models.DateField(
        verbose_name='дата поступелния',
        auto_now=True
    )

