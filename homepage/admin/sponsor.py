from django.contrib import admin
from homepage.models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'logo',
        'website_address',
        'activated_for_this_event',
    )
    list_display = (
        'name',
        'logo',
        'website_address',
        'activated_for_this_event',
    )
