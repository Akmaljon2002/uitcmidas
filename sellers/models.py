from django.db import models
from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    weight = models.CharField(max_length=20)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    photo = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name


