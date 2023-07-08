from django.contrib import admin
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

from .views import CustomPasswordChangeView, password_changed_done_view

urlpatterns = [
    path('', views.home,name="home"),
    path("about/", views.about,name="about"),
    path("contact/", views.contact,name="contact"),
    path("category/<int:val>",views.CategoryView.as_view(),name="category"),
    path("subcategory/<int:val1>/<int:val2>",views.SubCategoryView.as_view(),name="subcategory"),
    path("brandfilter/<str:bno>",views.brandfilter, name='brandfilter'),
    path("product-detail/<int:pk>",views.ProductDetail.as_view(),name="product-detail"),
    path('addadress/', views.addadress.as_view(), name='addadress'),
    path('viewprofile/',views.viewprofile.as_view(), name='viewprofile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    # path('updateprofile/',views.updateprofile.as_view(), name='updateprofile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    path('deleteAddress/<int:pk>', views.deleteAddress, name='deleteAddress'),
    # buy now
    path('buynow/<int:pk>', views.buynow, name='buynow'),
    # add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/',views.payment_done, name='paymentdone'),
    path('orders/',views.orders, name='orders'),

    path('search/', views.search, name='search'),
    path('wishlist/', views.show_wishlist, name='wishlist'),


    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),


    #login authentication
    path('registration/',views.CustomerRegistrationView.as_view(), name='customerregistration'),
    #inbuilt login view That's why don't need to write in view file
    path('accounts/login/', auth_view.LoginView.as_view(template_name='baseapp/login.html', authentication_form = LoginForm), name='login'),
    path('passwordchange/', CustomPasswordChangeView.as_view(), name='passwordchange'),
    path('passwordchangedone/', password_changed_done_view, name='passwordchangedone'),

    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    #password Reset /forgot password
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name ='baseapp/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name ='baseapp/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name ='baseapp/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name ='baseapp/password_reset_complete.html'), name='password_reset_complete'),

    
    #  path('test/<int:pk>',views.probymcate.as_view(),name="probymcate"),
    # path('test/1', views.fill),
      
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

admin.site.site_header = "Gogrocery"
admin.site.site_title = "Gogrocery"
