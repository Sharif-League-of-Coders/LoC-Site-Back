from django.contrib import admin
from apps.blog.models import Post,  Author


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'author')
    list_display_links = ('id',)
    list_editable = ('title', 'author')

    search_fields = ('title',)

    list_filter = ('author',)
    sortable_by = ('title', 'date')



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_display_links = ('id', 'first_name')

    sortable_by = ('first_name', 'last_name')
