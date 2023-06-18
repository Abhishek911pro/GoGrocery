from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES = (
('Bihar','Bihar'),
('Delhi','Delhi'),
('Gujrat','Gujrat'),
('Haryana','Haryana'),
('Assam','Assam'),
('Odisa','Odisa'),
('Punjab','Punjab'),
('West Bengal','West Bengal'),
('Rajasthan','Rajasthan'),
('Uttar Pradesh','Uttar Pradesh'),
    
)




class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name +" ("+str(self.id)+")"
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.name #+ "--" + self.category.name
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True,blank=True)
    main_category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,default='')
    selling_price = models.FloatField(blank=True)
    discounted_price = models.FloatField(blank=True)
    description = models.TextField(blank=True)
    other_info = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    product_image = models.ImageField(upload_to='product',blank=True)
    def __str__(self):
        return self.title +" ----- "+ str(self.sub_category)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10,default='M')
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True, null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product,on_delete= models.CASCADE)