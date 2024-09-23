from django.shortcuts import render,redirect
from .models import *
import random
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse,HttpResponse
import razorpay
import pkg_resources
# Create your views here.

def index(request):
    product = Product.objects.all()
    return render(request,'index.html',{"product":product})


def shop(request):
    product = Product.objects.all()
    return render(request,'shop.html',{"product":product})

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')



def checkout(request):
    return render(request,'checkout.html')

    

def profilepage(request):
    user = User.objects.get(email=request.session['email'])
    
    if request.method == "POST":
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.mobile = request.POST['mobile']
        user.countryName = request.POST['countryName']
        
        try:
            user.profile = request.FILES['profile']
            user.save()
            request.session['profile'] = user.profile.url 
            
        except:
            user.save()
            if user.usertype == "buyer":
                return redirect("index")
            else:
                return redirect("sindex")
    else:
        
        if user.usertype == "buyer":
            return render(request, 'profile.html', {'user': user})
        else:
            return render(request, 'Sellerprofile.html', {'user': user})
    
    


def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            msg  = "Email is already Exits! "
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],  
                    mobile = request.POST['mobile'],
                    password = request.POST['password'],
                    countryName = request.POST['countryName'],
                    profile = request.FILES['profile'],
                    usertype = request.POST['usertype']
                    
                )
                return render(request,'login.html')
            else:
                msg = "Password and confirm Password doesn't match!"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
    
def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            
            if user.password == request.POST['password']:
                request.session['email']= user.email
                request.session['profile'] = user.profile.url
                if user.usertype == "buyer":
                    return render(request,'index.html')
                else:
                    return render(request,'SellerIndex.html')

            else:
                msg = "Password doesn't match !!"
                return render(request,'login.html',{'msg':msg})
        except:
            msg = "Email dosen't match !!"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
    

def logout(request):
    del request.session['email']
    del request.session['profile']

    return redirect("login")

def cpass(request):
    user = User.objects.get(email=request.session['email'])
    if request.method=="POST":
        try:
            
            if user.password == request.POST['password']:
                if request.POST['npassword'] == request.POST['cpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    return redirect("logout")
                else:
                    msg = "Password And Confirm Passsword Doesn't Match "
                    if user.usertype =="buyer":
                        return render(request,'cpass.html',{"msg":msg})
                    else:
                        return render(request,'SellerCPassword.html',{"msg":msg})

                        
            else:
                msg = "Old Password Doesn't Match "
                if user.usertype == "buyer":
                   return render(request,'cpass.html',{"msg":msg})
                else:
                    return render(request,'SellerCPassword.html',{"msg":msg})
          
        except:
            if user.usertype == "buyer":
                return render(request,"cpass.html")
            else:
                return render(request,"SellerCPassword.html")
    
                    
    else:    
        if user.usertype == "buyer":        
            return render(request,"cpass.html")
        else:
            return render(request,"SellerCPassword.html")



def fpass(request):
    if request.method== "POST":
        
        try:
             
            user = User.objects.get(mobile = request.POST['mobile'])
            mobile = request.POST['mobile']
            otp = random.randint(1001,9999)
            
            resp = requests.post('https://textbelt.com/text', {
            'mobile': str(mobile),
            'message': otp,
            'key': 'textbelt',
        })
            request.session['mobile']=mobile
            request.session['otp'] = otp
            print(resp.json())
            return render(request,'otp.html')   

        except:
            msg = "Mobile Number Doesn't Exits!!" 
            return render(request,'fpass.html',{"msg":msg})  
    else:
        return render(request,'fpass.html')  

           


def otp(request):
    otp = int(request.session['otp'])
    uotp = int(request.POST['uotp'])
    try:
        
        if otp == uotp:
            del request.session['otp']
            return render(render,"newpass.html")
        else:
            msg = "Invalid otp!!"
            return render(request,"otp.html",{"msg":msg})
    except:
        return render(request,'otp.html')
    
    
    
#___________________________________________________________
#seller


def sindex(request):
    return render(request,"SellerIndex.html")

def Sellerlogin(request):
    return render(request,"Sellerlogin.html")

    




def addproduct(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        try:
           
            Product.objects.create(
                user=user,
                pcategory=request.POST['pcategory'],
                productname=request.POST['productname'],
                pprice=request.POST['pprice'],
                pdesc=request.POST['pdesc'],
                productimage=request.FILES['productimage'], 
            )
            return redirect("viewProduct")
        except Exception as e:
            print(e)
            msg = "Error adding product. Please try again."
            return render(request, "SellerIndex.html", {"msg": msg})
    return render(request, "SellerAddProducts.html")

    
def viewproduct(request):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.filter(user=user)
    return render(request, "ViewProduct.html", {"product":product})
    

def spdetails(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.filter(pk=pk)
    return render(request, "Spdetails.html", {"product":product})

def pupdate(request, pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    
    if request.method == "POST":
        product.pcategory = request.POST['pcategory']
        product.productname = request.POST['productname']
        product.pprice = request.POST['pprice']
        product.pdesc = request.POST['pdesc']
        
        try:
            if 'productimage' in request.FILES:
                product.productimage = request.FILES['productimage']
            product.save()
        except Exception as e:
            print(e)
            msg = "Error updating product. Please try again."
            return render(request, "ProductUpdate.html", {"product": product, "msg": msg})

        return redirect("viewproduct")
    else:
        return render(request, "ProductUpdate.html", {"product": product})

        
            
def delete(request, pk):
    user = User.objects.get(email=request.session['email'])
    try:
        product = Product.objects.get(pk=pk, user=user)
        product.delete()
        msg = "Product deleted successfully."
        return redirect("viewproduct")
    except Product.DoesNotExist:
        msg = "Product not found."
        return render(request, "Spdetails.html", {"msg": msg})
    except Exception as e:
        print(e)
        msg = "Error deleting product. Please try again."
        return render(request, "Spdetails.html", {"msg": msg})
    
    
    
def bpdetails(request,pk):
    if request.session.get('email'):
        user = User.objects.get(email=request.session['email'])
        product = Product.objects.get(pk=pk)
        w = False
        w1 = False
        try:
            wish = Wishlist.objects.get(user=user,product=product)
            w = True
        except:
            pass
        
        try:
            cart = Cart.objects.get(
            user = user,
            product = product,
            payment = True  
        )
            w1 = True
        except:
            pass
        
        return render(request, "bpdetails.html", {"product":product,"w":w,"w1":w1})
    else:
        return redirect('login')

    



def addwishlist(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    Wishlist.objects.create(
        user = user,
        product = product
    )
    return redirect("wishlist")

def wishlist(request):
    user = User.objects.get(email=request.session['email'])
    wish = Wishlist.objects.filter(
        user = user,
    )
    count = wish.count()
    return render(request, "wishlist.html", {'wish':wish,"count":count})


def deletewishlist(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    wish = Wishlist.objects.filter(
        user = user,
        product = product
        
    )
    wish.delete()
    return redirect('wishlist')



def cart(request):
    try:
        user = User.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(
        user = user,
        payment = False,
         )
        net = 0
        subtotal = 100

        for i in cart:
            net += i.roundtotal

        for i in cart:
            subtotal += i.roundtotal

        print("Net:", net)
        print("Subtotal:", subtotal)
        
        
        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': net * 100, 'currency': 'INR', 'payment_capture': 1})
        
        context = {
                        'payment': payment,
                        # 'book':book,  # Ensure the amount is in paise
                    }

            
        return render(request,'cart.html',{"cart":cart,"net":net,"subtotal":subtotal,"context":context})

    except:
        return render(request,'cart.html')

    
def addcart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    Cart.objects.create(
        user = user,
        product = product,
        payment = False,
        qty = 1,
        total = product.pprice,
        roundtotal = product.pprice,
    )
    return redirect("cart")

def deletecart(request,pk):
    user = User.objects.get(email=request.session['email'])
    product = Product.objects.get(pk=pk)
    cart = Cart.objects.filter(
        user = user,
        product = product
        
    )
    cart.delete()
    return redirect('cart')
      
       
        
def changeqty(request,pk):
    
    c = Cart.objects.get(pk=pk)    
    c.qty = int(request.POST['qty'])
    c.save()
    c.roundtotal = c.total*c.qty
    c.save()
    print(c.roundtotal)
    return JsonResponse({'roundtotal': c.roundtotal})


def thankyou(request):
    try:
        user = User.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(user=user)

        
        for i in cart:
            print("_______________")
            i.payment = True
            i.save()
        return render(request,'thankyou.html',{"cart":cart})

    except Exception as e:
        print(e)
        return render(request,'cart.html')

    
def myorder(request):
    user = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user,payment=True)
    return render(request,'myorder.html',{"cart":cart}) 

    

    
    
        