from django import forms
from . import models


class ExpencesForms(forms.ModelForm):
    class Meta:
        model = models.IncomeAndExpediture
        fields = ('name','value','status')


class SalaryForms(forms.ModelForm):
    class Meta:
        model = models.Salary 
        fields = ('name','value')