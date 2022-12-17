from django.contrib import admin
from . import models

class IncomeAndExpeditureAdmin(admin.ModelAdmin):
    list_display = ('user','name','value','date','status')

class SalaryAdmin(admin.ModelAdmin):
    list_display =('user','name','value', 'date')


admin.site.register(models.IncomeAndExpediture,IncomeAndExpeditureAdmin)
admin.site.register(models.Salary, SalaryAdmin)