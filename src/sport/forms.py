from django import forms
from . import models

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = models.SubscriptionModel
        fields = ('name', 'quantity','status')


class SubscriptionVisitsForm(forms.ModelForm):
    class Meta:
        model = models.SubscriptionVisit
        fields = ('info','subscription')