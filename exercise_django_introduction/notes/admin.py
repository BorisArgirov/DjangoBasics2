from django.contrib import admin

from notes.models import Note


# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['priority']

