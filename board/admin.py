from django.contrib import admin
from .models import Categories, Announcements, ResponseStatus, Response


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    list_display_links = ('id', 'name') 


@admin.register(Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'author', 'date_publication')
    list_filter = ('category',)

@admin.register(ResponseStatus)
class ResponseStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'announcements', 'user', 'status')
    list_editable = ('status',)