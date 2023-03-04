from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableAdminMixin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Place, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    fields = ['place', 'image', 'get_preview']
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return format_html(
            '<img src="{}" width="auto" height="200px" />', obj.image.url
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', ]
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
