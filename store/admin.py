from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'category', 'created_at']
    list_filter = ['category']
    list_editable = ['price', 'stock']

admin.site.register(CartItem)
