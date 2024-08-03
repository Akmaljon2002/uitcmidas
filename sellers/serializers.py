from rest_framework.serializers import Serializer, ModelSerializer

from sales.models import ProductSale, Delivery, Sale
from .models import Category, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def update(self, instance, validated_data):
        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)
        return super().update(instance, validated_data)


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ('seller', )

    def update(self, instance, validated_data):
        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)
        return super().update(instance, validated_data)


class SellerProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SellerProductSaleSerializer(ModelSerializer):
    product = SellerProductSerializer()

    class Meta:
        model = ProductSale
        exclude = ('client', )


class SellerDeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class SellerSalesSerializer(ModelSerializer):
    carts = SellerProductSaleSerializer(many=True)
    delivery = SellerDeliverySerializer(default=None)

    class Meta:
        model = Sale
        fields = ("id", "payment_status", 'status', 'total_price', 'count', "comment", "carts", "delivery")
        extra_kwargs = {
            'carts': {'read_only': True},
        }

