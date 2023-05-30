from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart = models.ManyToManyField('Product',blank=True)
    pic = models.CharField(max_length=500,default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    my_orders = models.ManyToManyField('Order',blank=True)
    address = models.ForeignKey("Address",null=True,on_delete=models.SET_NULL,blank=True)

    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=500,blank=True,null=True)
    seller = models.EmailField(null=True)
    images = models.CharField(max_length=10000,null=True)
    size = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey("Category",on_delete=models.SET_NULL,null=True)
    gender = models.ForeignKey('Gender',on_delete=models.SET_NULL,blank=True,null=True)

    @property
    def get_images(self):
        image_list = self.images.split(" | ")
        return image_list

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    @property
    def get_products(self):
        products = Product.objects.filter(category_id=self.pk)
        return products
    
    
class Gender(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    buyer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    ordered_date = models.DateField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False, null=True)
    is_cancelled = models.BooleanField(default=False, null=True)
    delivery_address = models.ForeignKey('Address',null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.buyer.user.username + " | " + self.product.name


class Address(models.Model):
    name = models.CharField(max_length=500,blank=True)
    phone_number = models.IntegerField(blank=True)
    house_name = models.CharField(max_length=500,blank=True)
    street_name = models.CharField(max_length=500,blank=True)
    state_name = models.CharField(max_length=500,blank=True)
    pincode = models.IntegerField(blank=True)
    landmark = models.CharField(max_length=500,blank=True,null=True)
    town_city = models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return self.name + " | " + self.house_name

