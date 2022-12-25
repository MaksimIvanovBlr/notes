from django.contrib import admin
from . import models


class IncomeAndExpeditureAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value', 'date', 'status')


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value', 'date')


class PerDayAdmin(admin.ModelAdmin):
    list_display = ('user', 'value')


class ReservAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'date')


class AdditionalIncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value', 'date')


admin.site.register(models.IncomeAndExpediture, IncomeAndExpeditureAdmin)
admin.site.register(models.Salary, SalaryAdmin)
admin.site.register(models.PerDay, PerDayAdmin)
admin.site.register(models.Reserv, ReservAdmin)
admin.site.register(models.AdditionalIncome, AdditionalIncomeAdmin)
