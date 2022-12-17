from django.contrib import admin
from . import models

class IncomeAndExpeditureAdmin(admin.ModelAdmin):
    list_display = ('user','name','value','date','status')




admin.site.register(models.IncomeAndExpediture,IncomeAndExpeditureAdmin)
