from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    fields = ['place', 'image', 'get_preview']
    readonly_fields = ['get_preview']

    def get_preview(self, place):
        return format_html(
            '<img src="{}" width="auto" height="200px" />', place.image.url
        )

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass