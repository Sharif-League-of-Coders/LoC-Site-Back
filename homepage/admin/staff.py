from django.contrib import admin
from homepage.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'position',
        'image',
        'email',
        'show_in_homepage',
    )
    list_display = (
        'name',
        'position',
        'image',
        'email',
        'show_in_homepage',
    )
