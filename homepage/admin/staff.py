from django.contrib import admin
from homepage.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass
