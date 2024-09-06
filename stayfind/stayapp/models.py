from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
import random
import string

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

class CustomUser(AbstractUser):
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)

    def generate_reset_token(self):
        self.reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        self.reset_token_expiry = timezone.now() + timedelta(minutes=30)
        self.save()

    # Add related_name to avoid clashes with Django's default User model
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Updated related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Updated related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )