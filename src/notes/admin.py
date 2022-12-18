from django.contrib import admin
from . import models

class NotesAdmin(admin.ModelAdmin):
    list_display = ('user','text', 'create_date','update_date')

admin.site.register(models.Notes, NotesAdmin)