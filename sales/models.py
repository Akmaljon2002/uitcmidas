from django.db import models
from sellers.models import Product
from user.models import CustomUser


class ProductSale(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="carts")
    count = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        return self.product.name


class Delivery(models.Model):
    street = models.CharField(max_length=100)
    flat = models.CharField(max_length=20)
    flat_number = models.IntegerField()
    comment = models.TextField(default="")

    def __str__(self):
        return self.street


class Sale(models.Model):
    ChoicePayment = (
        ("card_bank", "card_bank"),
        ("card_courier", "card_courier"),
        ("cash_courier", "cash_courier"),
    )
    ChoiceStatus = (
        ("waiting", "waiting"),
        ("preparing", "preparing"),
        ("delivering", "delivering"),
        ("delivered", "delivered"),
    )
    client = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    carts = models.ManyToManyField(ProductSale, related_name="sales")
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, blank=True, null=True)
    count = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()
    payment_status = models.CharField(max_length=25, choices=ChoicePayment)
    comment = models.TextField(default="")
    status = models.CharField(max_length=50, choices=ChoiceStatus, default='waiting')
    seller_id = models.IntegerField(default=0)

    def __str__(self):
        return self.client.full_name
