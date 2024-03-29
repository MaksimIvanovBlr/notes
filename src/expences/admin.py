from django.contrib import admin
from . import models


class ExpeditureAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value', 'date', 'status')


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value', 'date')


class PerDayAdmin(admin.ModelAdmin):
    list_display = ('user', 'value')


class ReservAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'date')


class AdditionalIncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'value', 'date')

class DailyConsumptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'per_month', 'buffer_money')


admin.site.register(models.Expediture, ExpeditureAdmin)
admin.site.register(models.Salary, SalaryAdmin)
admin.site.register(models.PerDay, PerDayAdmin)
admin.site.register(models.Reserv, ReservAdmin)
admin.site.register(models.AdditionalIncome, AdditionalIncomeAdmin)
admin.site.register(models.DailyConsumption, DailyConsumptionAdmin)