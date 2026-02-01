from django.contrib import admin
from .models import Ingredient, PotionResult

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(PotionResult)
class PotionResultAdmin(admin.ModelAdmin):
    list_display = ("title",)
    filter_horizontal = ("ingredients",)