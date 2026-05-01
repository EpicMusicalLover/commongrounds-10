from django.contrib import admin
from .models import ProductType, Product, Transaction


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('name','product_type','owner','price','stock','status',)
    list_filter = ('status', 'product_type')
    search_fields = ('name', 'description')
    fieldsets = [
        ('Basic Info', {
            'fields': ['name', 'product_type', 'owner']
        }),
        ('Details', {
            'fields': ['description', 'product_image']
        }),
        ('Pricing & Stock', {
            'fields': ['price', 'stock', 'status']
        }),
    ]

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('buyer','product','amount','status','created_on',)
    list_filter = ('status', 'created_on')
    search_fields = ('buyer__user__username', 'product__name')
    fieldsets = [
        ('Transaction Info', {
            'fields': ['buyer', 'product', 'amount']
        }),
        ('Status', {
            'fields': ['status']
        }),
        ('Metadata', {
            'fields': ['created_on']
        }),
    ]


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
