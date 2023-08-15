from django.contrib import admin
from .models import Category, Product, Customer, Review, Order, User_login, Status
from PIL import Image
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_featured', 'category', 'stock', 'description', 'avg_rating']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    list_filter = ['is_featured', 'category', 'stock']



class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'date_posted', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__username', 'product__name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone', 'is_active')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_price', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__user__username')

class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_date')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)




admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(User_login)
admin.site.register(Status)
admin.site.register(Product)
