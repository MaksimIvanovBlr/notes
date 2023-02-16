from django import forms
from . import models


class ExpencesForm(forms.ModelForm):
    class Meta:
        model = models.Expediture
        fields = ('name', 'value', 'status', 'description')


class SalaryForm(forms.ModelForm):
    class Meta:
        model = models.Salary
        fields = ('name', 'value', 'status')


class PerDayForm(forms.ModelForm):
    class Meta:
        model = models.PerDay
        fields = ('value', 'day', 'salary_method', 'balance')


class ReservForm(forms.ModelForm):
    class Meta:
        model = models.Reserv
        fields = ('value',)


class AdditionalIncomeForm(forms.ModelForm):
    class Meta:
        model = models.AdditionalIncome
        fields = ('name', 'value', 'status')


class DailyConsumptionForm(forms.ModelForm):
    class Meta:
        model = models.DailyConsumption
        fields = ('buffer_money',)