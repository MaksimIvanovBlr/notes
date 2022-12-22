from django import forms
from . import models


class ExpencesForm(forms.ModelForm):
    class Meta:
        model = models.IncomeAndExpediture
        fields = ('name','value','status', 'description')


class SalaryForm(forms.ModelForm):
    class Meta:
        model = models.Salary 
        fields = ('name','value','status')


class  PerDayForm(forms.ModelForm):
    class Meta:
        model = models.PerDay 
        fields = ('value',)

class  ReservForm(forms.ModelForm):
    class Meta:
        model = models.Reserv 
        fields = ('value',)


class AdditionalIncomeForm(forms.ModelForm):
    class Meta:
        model = models.AdditionalIncome
        fields = ('name','value')