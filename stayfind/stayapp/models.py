from django.db import models
from django.utils import timezone
from django.conf import settings

class Product(models.Model):
    CITY = ((1, 'Delhi'), (2, 'Pune'), (3, 'Bangalore'), (4, 'Mumbai'))
    name = models.CharField(max_length=20, verbose_name='Hotel Name')
    city = models.IntegerField(verbose_name='City', choices=CITY)
    price = models.IntegerField()
    para = models.CharField(max_length=2000)
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to='image')
    pimage2 = models.ImageField(upload_to='image')

class Cart(models.Model):
    uid = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='uid')
    pid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='pid')
    qty = models.IntegerField(default=1)
    checkin = models.DateField(default=timezone.now)
    checkout = models.DateField(default=timezone.now)

class Order(models.Model):
    uid = models.ForeignKey('auth.User', on_delete=models.CASCADE, db_column='uid')
    pid = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='pid')
    qty = models.IntegerField(default=1)
    amt = models.IntegerField()

class Orderhistory(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()
