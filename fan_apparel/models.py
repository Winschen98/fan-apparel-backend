from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxCost = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingCost = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalCost = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = name = models.CharField(max_length=200, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.name)
