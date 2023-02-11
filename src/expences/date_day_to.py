from datetime import datetime
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

user_s = get_user_model()
user1 = User
date = datetime.now()


class ToSalary():
    now_date = datetime.now()
    #for testing
    # now_date = datetime(2023,1,11)
    # user_date = user1.user_per_day
    user_date = 1
    some_date2 = datetime(now_date.year, now_date.month, user_date)

    if now_date.month == 12:
        some_date = datetime(now_date.year + 1, 1, user_date)
    else:
        some_date = datetime(now_date.year, now_date.month + 1, user_date)

    @property
    def days_to_salary(self):
        if self.now_date.day < self.some_date.day:
            day = self.some_date2 - self.now_date
        else:
            day = self.some_date - self.now_date

        return day.days

