from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Brand, Cart, Category, Customer, OrderPlaced, Payment,SubCategory,Product, Wishlist

# Register your models here.
admin.site.unregister(Group)
admin.site.register(Category)
admin.site.register(SubCategory)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','main_category','product_image']

@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['id','name']


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
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']