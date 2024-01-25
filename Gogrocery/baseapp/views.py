from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import View
import razorpay

from .models import STATE_CHOICES, Brand, Cart, Category, Customer, OrderPlaced, Payment,SubCategory,Product, Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import MyPasswordChangeForm
# Create your views here.


def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
   # num = Product.objects.exclude(sub_category=None)
    product = Product.objects.all()
    states = STATE_CHOICES
    return render(request, "baseapp/home.html",locals())


def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    brand = Brand.objects.all()
    return render(request, "baseapp/about.html",locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "baseapp/contact.html",locals())


class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        category = Category.objects.all()
        subcategory = SubCategory.objects.filter(category_id= val)
        product = Product.objects.filter(main_category=val)
        
        #sublist badge count
        subcateCount = SubCategory.objects.filter(category_id= val).count()
        #getting the name of subcategory in a list
        namelist = []
        for j in subcategory:
            namelist.append(j.name)
        #counting the number of products in each subcategory and putting it in a list
        pcounts = []
        for i in subcategory:
            prodcount = Product.objects.filter(sub_category_id = i.id).count()
            pcounts.append(prodcount)
        #merging both lists
        sublist = [[x, y] for x, y in zip(namelist, pcounts)]
        
        #for brand sublist
        brand = Brand.objects.all()

        #getting the name of subcategory in a list
        brandnamelist = []
        for j in brand:
            brandnamelist.append(j.name)
        #counting products is brands
        bprod = []
        for i in brand:
            countprod = Product.objects.filter(brands_id = i.id).count()
            bprod.append(countprod)
        #merging both lists
        brandlist = [[x, y] for x, y in zip(brandnamelist, bprod)]

        return render(request, "baseapp/category.html",locals())

class SubCategoryView(View):
    def get(self,request,val1,val2):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        category = Category.objects.all()
        subcategory = SubCategory.objects.filter(category_id=val1)
        product = Product.objects.filter(sub_category=val2)

        #sublist badge count
        #count product for subcategory list
        subcateCount = SubCategory.objects.filter(category_id= val1).count()
        #getting the name of subcategory in a list
        namelist = []
        for j in subcategory:
            namelist.append(j.name)
        #counting the number of products in each subcategory and putting it in a list
        pcounts = []
        for i in subcategory:
            prodcount = Product.objects.filter(sub_category_id = i.id).count()
            pcounts.append(prodcount)
        #merging both lists
        sublist = [[x, y] for x, y in zip(namelist, pcounts)]
        
        #for brand sublist
        brand = Brand.objects.all()

        #getting the name of subcategory in a list
        brandnamelist = []
        for j in brand:
            brandnamelist.append(j.name)
        #counting products is brands
        bprod = []
        for i in brand:
            countprod = Product.objects.filter(brands_id = i.id).count()
            bprod.append(countprod)
        #merging both lists
        brandlist = [[x, y] for x, y in zip(brandnamelist, bprod)]


        return render(request, "baseapp/subcategory.html",locals())
    
def brandfilter(request,bno):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    bname =  Brand.objects.filter(id=bno)   
    filtered_products = Product.objects.filter(brands=bno)
    return render(request, "baseapp/brandfilter.html",locals())


   
class ProductDetail(View):
    def get(self,request,pk):
        totalitem = 0
        wishitem = 0
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        
        return render(request,"baseapp/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'baseapp/customerregistration.html',locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registration Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'baseapp/customerregistration.html',locals())
    
class addadress(View):
    def get(self,request):
            totalitem = 0
            wishitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
                wishitem = len(Wishlist.objects.filter(user=request.user))
            form = CustomerProfileForm()
            return render(request, 'baseapp/addadress.html',locals())
            
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            username = request.user.username
            email = request.user.email
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'baseapp/addadress.html',locals())
    
def address(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'baseapp/address.html',locals())

#mycode
class viewprofile(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        if request.user.is_authenticated:
            form= EditUserProfileForm(instance=request.user) 
            return render(request, 'baseapp/viewprofile.html',locals())
        
    
    
def edit_profile(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditUserProfileForm(request.POST,instance=request.user)
            if form.is_valid():
                messages.success(request,"Updated Profile Save Successfully")
                form.save()
        else:
            form= EditUserProfileForm(instance=request.user)
        return render(request, 'baseapp/edit_profile.html',locals())

    
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'baseapp/changepassword.html'
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('passwordchangedone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        totalitem = 0
        wishitem = 0
        if self.request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=self.request.user))
            wishitem = len(Wishlist.objects.filter(user=self.request.user))
        context['totalitem'] = totalitem
        context['wishitem'] = wishitem
        return context

def password_changed_done_view(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'baseapp/passwordchangedone.html',locals())

#mycodeend


class updateAddress(View):
    def get(self,request,pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance = add)
        return render(request, 'baseapp/updateAddress.html',locals())
    
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            #getting data to add
            add = Customer.objects.get(pk=pk)
            #updating new value
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
def deleteAddress(request,pk):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    print(pk)
    if Customer.objects.get(pk=pk):

        add = Customer.objects.get(pk=pk)
        add.delete()
        return redirect('address')
    else:
         messages.warning(request,"no address available")

@login_required
def add_to_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    cart = Cart.objects.filter(user=user, product=product).first()
    if cart:
        # If the product is already in the cart, update the quantity
        cart.quantity += 1
        cart.save()
    else:
        # If the product is not in the cart, add it to the cart
        Cart(user = user,product=product).save()
    return redirect("/cart")



@login_required    
def show_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40  
    return render(request, 'baseapp/addtocart.html',locals())

@login_required
def buynow(request,pk):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    # product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=pk)

    cart = Cart.objects.filter(user=user, product=product).first()
    if cart:
        # If the product is already in the cart, update the quantity
        cart.quantity += 1
        cart.save()
    else:
        # If the product is not in the cart, add it to the cart
        Cart(user = user,product=product).save()
    return redirect("/checkout")

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request,"baseapp/wishlist.html",locals())




class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12" }
        payment_response = client.order.create(data=data)
        #print(payment_response)
        # {'id': 'order_M2fzVreqWqkoYO', 'entity': 'order', 'amount': 19500, 'amount_paid': 0, 'amount_due': 19500, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1686934864}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            
            payment.save()
        flag = 0
        return render(request, 'baseapp/checkout.html',locals())

@login_required    
def payment_done(request):

    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    print(cust_id)
    #print("payment_done : oid = ",order_id," pid = ",payment_id," cid = ",cust_id)
    user = request.user
    #return redirect("order")
    #customer = Customer.objects.get(user=user)
    customer = Customer.objects.get(id=cust_id)
    #to update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    #to save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        print("saved data in order placed")
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")

def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    orderDate = []
    for i in order_placed:
        orderDate.append(i.ordered_date.date())
    orderDate = list(set(orderDate))
    return render(request, 'baseapp/orders.html',locals())

def orderbydate(request, date):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    orderDate = []
    for i in order_placed:
        orderDate.append(i.ordered_date.date())
    orderDate = list(set(orderDate))
    
    newOrderplaced = []
    for i in order_placed:
        if date == str(i.ordered_date.date()):
            newOrderplaced.append(i)

    return render(request, 'baseapp/orderDate.html',locals())



@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get( Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40 
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40 
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required    
def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40 
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

@login_required    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist Remove Successfully',
        }
        return JsonResponse(data)

def search(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query)) #field lookup
    return render(request,"baseapp/search.html",locals())
    

