from django.contrib import admin
from .models import Graphic, Category


class GraphicAdmin(admin.ModelAdmin):
    """list display tuple"""
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        'size',
        'orientation',
    )

    # tuple, -sku for reverse order
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    """categories"""
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Graphic, GraphicAdmin)
admin.site.register(Category, CategoryAdmin)
