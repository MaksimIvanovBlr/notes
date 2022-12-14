from django import forms
from . import models


class ExpensesForm(forms.ModelForm):
    class Meta:
        model = models.Expenses
        fields = '__all__'

class AdvanceForm(forms.ModelForm):
    class Meta:
        model = models.Advance
        fields = '__all__'

class SalaryForm(forms.ModelForm):
    class Meta:
        model = models.Salary
        fields = '__all__'

