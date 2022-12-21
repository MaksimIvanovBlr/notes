from django import forms
from . import models


class ExpencesForms(forms.ModelForm):
    class Meta:
        model = models.IncomeAndExpediture
        fields = ('name','value','status', 'description')


class SalaryForms(forms.ModelForm):
    class Meta:
        model = models.Salary 
        fields = ('name','value','status')


class  PerDayForms(forms.ModelForm):
    class Meta:
        model = models.PerDay 
        fields = ('value',)

class  ReservForms(forms.ModelForm):
    class Meta:
        model = models.Reserv 
        fields = ('value',)