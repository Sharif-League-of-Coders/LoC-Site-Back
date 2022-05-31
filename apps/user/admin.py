from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import User, Person


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'is_active', 'is_superuser', 'persono', 'team']
    # list_editable = []
    # list_display_links = []
    search_fields = ['email']
    # sortable_by = []
    # list_filter = []

@admin.register(Person)
class ProfileAdmin(ModelAdmin):
    # inlines = (SkillInline, JobExperienceInline)
    list_display = ('id', 'firstname', 'lastname', 'birthdate', 'phonenumber',
                    'stu_number', 'user')

    # list_filter = ('university', 'major', 'university_degree')

    search_fields = ('firstname', 'lastname',
                     'phonenumber', )
