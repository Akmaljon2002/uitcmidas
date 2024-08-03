from django.contrib.auth.hashers import make_password
from rest_framework.serializers import Serializer, ModelSerializer, IntegerField, CharField
from sellers.models import Product
from user.models import CustomUser


class ProductAdminSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)
        return super().update(instance, validated_data)


class SellerSerializer(ModelSerializer):
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
