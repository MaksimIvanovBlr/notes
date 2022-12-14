from datetime import datetime
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

user_s = get_user_model()
user1 = User
date = datetime.now()


class ToSalary():
    now_date = datetime.now()
    some_date2 = datetime(now_date.year, now_date.month, 11)

    if now_date.month == 12:
        some_date = datetime(now_date.year + 1, 1, 11)
    else:
        some_date = datetime(now_date.year, now_date.month + 1, 11)

    @property
    def days_to_salary(self):
        if self.now_date.day < self.some_date.day:
            day = self.some_date2 - self.now_date
        else:
            day = self.some_date - self.now_date

        return day.days


# def calculated_month():
#     global date
#     date_calc = datetime(date.year, date.month, 11)


# class CalculatedMonth():
#     date = datetime.now()

#     date_calc_z = datetime(date.year, date.month, 20)
#     date_calc_a = datetime(date.year, date.month, 11)
    
