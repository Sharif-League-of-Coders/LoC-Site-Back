from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from .models import Team, Invitation


class InvitationInline(admin.StackedInline):
    model = Invitation


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ('id', 'name', 'creator', )
    search_fields = ('name', 'creator', )
    list_editable = ('name', )
    # list_filter = ()
    inlines = (InvitationInline, )


admin.site.register(Invitation)


@admin.register(Invitation)
class InvitationAdmin(ModelAdmin):
    list_display = ('id', 'user', 'team', 'type', 'status')
    list_filter = ('type', 'status')
