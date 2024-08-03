from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer, Serializer, CharField, DictField, BooleanField, \
    ListField, IntegerField, ValidationError

from sales.models import ProductSale, Delivery, Sale
from sellers.models import Category, Product
from user.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'phone', 'email', 'password', 'role',
                  'is_active')
        extra_kwargs = {
            'is_active': {'read_only': True},
            'role': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        instance = super().update(instance, validated_data)
        return instance


class CustomUserTokenSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginResponseSerializer(Serializer):
    refresh = CharField()
    access = CharField()
    user = CustomUserSerializer()


class CreateUserResponseSerializer(Serializer):
    refresh = CharField()
    access = CharField()
    user = CustomUserSerializer()


class ErrorValSer(Serializer):
    detail = DictField(child=ListField())


class UserCreateSerializer(ModelSerializer):
    phone = CharField(max_length=9, validators=[MinLengthValidator(9), MaxLengthValidator(9)])
    password = CharField(max_length=255)
    full_name = CharField(max_length=50)
    email = CharField(max_length=50)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = CustomUser
        fields = ['phone', 'password', 'full_name', 'email']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name']


class UserLoginSerializer(Serializer):
    phone = CharField(max_length=9, validators=[MinLengthValidator(9), MaxLengthValidator(9)])
    password = CharField(max_length=255)


class UserCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSaleSerializer(ModelSerializer):
    class Meta:
        model = ProductSale
        fields = ("product", "count")


class ProductUpdateSaleSerializer(ModelSerializer):
    class Meta:
        model = ProductSale
        fields = ("count", )


class ProductSaleSerializer(ModelSerializer):
    product = UserProductSerializer()

    class Meta:
        model = ProductSale
        exclude = ('client', )


class DeliverySerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class SaleCreateSerializer(ModelSerializer):
    cart_ids = ListField(child=IntegerField())
    delivery = DeliverySerializer(default=None)

    class Meta:
        model = Sale
        fields = ("client", "cart_ids", "carts", "delivery", "payment_status", "comment")
        extra_kwargs = {
            'client': {'read_only': True},
            'carts': {'read_only': True},
        }

    @transaction.atomic()
    def create(self, validated_data):
        cart_ids = validated_data.pop('cart_ids')
        delivery_data = validated_data.pop('delivery')
        total_price = 0
        total_count = 0
        carts = []
        seller_id = 0
        for cart_id in cart_ids:
            cart = get_object_or_404(ProductSale, id=cart_id, client=self.context['request'].user)
            if seller_id:
                if seller_id != cart.product.seller.id:
                    raise ValidationError("All carts must have the same seller.")
            seller_id = cart.product.seller.id
            total_price += cart.price
            total_count += 1
            carts.append(cart)
        if delivery_data:
            delivery = Delivery.objects.create(**delivery_data)
        else:
            delivery = None

        sale = Sale.objects.create(
            client=self.context['request'].user,
            total_price=total_price,
            count=total_count,
            delivery=delivery,
            seller_id=seller_id,
            **validated_data
        )

        sale.carts.set(carts)
        return sale


class SalesSerializer(ModelSerializer):
    carts = ProductSaleSerializer(many=True)
    delivery = DeliverySerializer(default=None)

    class Meta:
        model = Sale
        fields = ("id", "payment_status", 'status', 'total_price', 'count', "comment", "carts", "delivery")
        extra_kwargs = {
            'carts': {'read_only': True},
        }


