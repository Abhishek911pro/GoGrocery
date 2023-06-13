from django.shortcuts import redirect, render
from django.views import View
from .models import Category, Customer,SubCategory,Product
from .forms import CustomerRegistrationForm, CustomerProfileForm, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
   # num = Product.objects.exclude(sub_category=None)
    product = Product.objects.all()
    return render(request, "baseapp/home.html",locals())

def about(request):
    return render(request, "baseapp/about.html")

def contact(request):
    return render(request, "baseapp/contact.html")


class CategoryView(View):
    def get(self,request,val):
        category = Category.objects.all()
        subcategory = SubCategory.objects.filter(category_id= val)
        print(subcategory)
        product = Product.objects.filter(main_category=val)
        #title = SubCategory.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, "baseapp/category.html",locals())

class SubCategoryView(View):
    def get(self,request,val1,val2):
        category = Category.objects.all()
        subcategory = SubCategory.objects.filter(category_id=val1)
        product = Product.objects.filter(sub_category=val2)
        return render(request, "baseapp/subcategory.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
       # wishlist = Wishlist.objects.filter(product=product)
       # wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
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
    add = Customer.objects.filter(user=request.user)
    return render(request, 'baseapp/address.html',locals())

#mycode
class viewprofile(View):
    def get(self,request):
        if request.user.is_authenticated:
            form= EditUserProfileForm(instance=request.user) 
            return render(request, 'baseapp/viewprofile.html',locals())
    
    
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditUserProfileForm(request.POST,instance=request.user)
            if form.is_valid():
                messages.success(request,"Updated Profile Save Successfully")
                form.save()
        else:
            form= EditUserProfileForm(instance=request.user)
        return render(request, 'baseapp/edit_profile.html',locals())

#mycodeend


class updateAddress(View):
    def get(self,request,pk):
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
    print(pk)
    if Customer.objects.get(pk=pk):

        add = Customer.objects.get(pk=pk)
        add.delete()
        return redirect('address')
    else:
         messages.warning(request,"no address available")
    
    

