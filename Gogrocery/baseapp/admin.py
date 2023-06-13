from django.contrib import admin
from .models import Category, Customer,SubCategory,Product

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','zipcode']

