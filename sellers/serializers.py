from rest_framework.serializers import Serializer, ModelSerializer
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
