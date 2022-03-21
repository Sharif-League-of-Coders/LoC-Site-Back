from django.contrib import admin
from homepage.models import Home


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    fields = (
        'about_this_event',
        'activate',
        'number',
    )
    list_display = (
        'number',
        'activate',
        'about_this_event',
    )
