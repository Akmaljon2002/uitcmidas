from rest_framework.serializers import Serializer, ModelSerializer, IntegerField, CharField
from sellers.models import Product


class ProductAdminSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def update(self, instance, validated_data):
        photo = validated_data.get('photo', None)
        if photo is None:
            validated_data.pop('photo', None)
        return super().update(instance, validated_data)