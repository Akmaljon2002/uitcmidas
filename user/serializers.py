from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework.serializers import ModelSerializer, Serializer, CharField, DictField, BooleanField
from user.models import CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'phone', 'email', 'password',
                  'is_active')
        extra_kwargs = {
            'is_active': {'read_only': True},
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
    detail = CharField()
    success = BooleanField()
    refresh = CharField()
    access = CharField()
    user = CustomUserSerializer()


class ErrorResponseSerializer(Serializer):
    detail = CharField()
    success = BooleanField()
    data = DictField(child=CharField())


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


class UserGetCurrentSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'phone', 'email')

