"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin    
from django.urls import path,include
from. import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('shop/', views.shop, name='shop'),  # for shop.html
    path('about/', views.about, name='about'),  # for about.html
    path('services/', views.services, name='services'),  # for services.html
    path('blog/', views.blog, name='blog'),  # for blog.html
    path('contact/', views.contact, name='contact'),  # for contact.html
    path('cart/', views.cart, name='cart'), 
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('cpass/', views.cpass, name='cpass'),
    path('signup/', views.signup, name='signup'),
    path('fpass/', views.fpass, name='fpass'),
    path('otp/', views.otp, name='otp'),
    path('profile/', views.profilepage, name='profilepage'),
    path('checkout/', views.checkout, name='checkout'),

    
    
    #=======================================================
    #seller
    
    path('Sellerlogin', views.Sellerlogin, name='Sellerlogin'),
    # path('Sellerprofilepage/', views.Sellerprofilepage, name='Sellerprofilepage'),

    path('sindex/', views.sindex, name='sindex'),
    path('addProduct/', views.addproduct, name='addproduct'),
    path('viewproduct/', views.viewproduct, name='viewproduct'),
    path('spdetails/<int:pk>', views.spdetails, name='spdetails'),
    path('pupdate/<int:pk>', views.pupdate, name='pupdate'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('bpdetails/<int:pk>', views.bpdetails, name='bpdetails'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('addwishlist/<int:pk>', views.addwishlist, name='addwishlist'),
    path('deletewishlist/<int:pk>', views.deletewishlist, name='deletewishlist'),

    path('cart', views.cart, name='cart'),
    path('addcart/<int:pk>', views.addcart, name='addcart'),
    path('deletecart/<int:pk>', views.deletecart, name='deletecart'),
    path('changeqty/<int:pk>', views.changeqty, name='changeqty'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('myorder', views.myorder, name='myorder'),








    
    


]