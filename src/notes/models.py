from django.db import models
from django.contrib.auth import get_user_model

user_n = get_user_model()


class Notes(models.Model):
    user = models.ForeignKey(
        user_n,
        verbose_name='Пользователь',
        related_name='user_notes',
        on_delete=models.PROTECT
    )
    text = models.TextField(
        verbose_name='Заметка'
    )
    create_date = models.DateField(
        verbose_name='Дата создания',
        auto_now=False,
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        verbose_name='Время изменения',
        auto_now=True
    )
