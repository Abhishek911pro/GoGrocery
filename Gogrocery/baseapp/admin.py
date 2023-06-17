from django.contrib import admin
from .models import Cart, Category, Customer, OrderPlaced, Payment,SubCategory,Product

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer_name','product','quantity','ordered_date','status','payment']

    def customer_name(self, obj):
        return obj.customer.name

    customer_name.short_description = 'Customer'