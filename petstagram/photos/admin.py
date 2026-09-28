from django.contrib import admin

from pets.models import Pet
from photos.models import Photo


# Register your models here.

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['location', 'date_of_publication', 'tagged_pets_list']

    @staticmethod
    def tagged_pets_list(obj):
        return ', '.join(p.name for p in obj.tag_pets.all())