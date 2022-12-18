from django import forms
from . import models



class NotesForm(forms.ModelForm):
    class Meta:
        model = models.Notes
        fields = ('text',)