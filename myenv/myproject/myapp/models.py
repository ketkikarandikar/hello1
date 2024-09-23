from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    mobile = models.BigIntegerField()
    countryName = models.CharField(max_length=20)
    profile = models.ImageField(default="",upload_to="picture/")
    usertype = models.CharField(max_length=20,default="buyer")
    
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    category = (
        ("Sofa","Sofa"),
        ("Coffee Table","Coffee Table"),
        ("TV Stand","TV Stand"),
        ("Armchair","Armchair"),
        ("Bookshelf","Bookshelf"),
        ("Bed Frame","Bed Frame"),
        ("Mattress","Mattress"),
        ("Mirror","Mirror"),
        ("Dining Table","Dining Table"),
        ("Sideboard","Sideboard"),
        ("Server Table","Server Table"),
        ("Dining Chairs","Dining Chairs"),
        
    )
    pcategory = models.CharField(max_length=50,choices=category)
    productname = models.CharField(max_length=50)
    pprice = models.PositiveIntegerField()
    pdesc = models.TextField()
    productimage = models.ImageField(default="", upload_to="picture/pimages")
    
    def __str__(self):
        return self.productname
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    time_date = models.DateTimeField(default=timezone.now())

    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    time_date = models.DateTimeField(default=timezone.now())
    payment = models.BooleanField(default=False)
    qty = models.IntegerField(default=1)
    total = models.IntegerField()
    roundtotal = models.IntegerField()


    
    