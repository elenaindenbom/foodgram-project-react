from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, IngredientAmount, ShoppingCart,
                     Favorite)

admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(IngredientAmount)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'in_favorites')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('in_favorites',)

    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
