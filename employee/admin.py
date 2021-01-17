from django.contrib import admin
from .models import LeaveModel


# Register your models here.

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'is_approve')

    class Meta:
        model = LeaveModel


admin.site.register(LeaveModel, LeaveAdmin)
