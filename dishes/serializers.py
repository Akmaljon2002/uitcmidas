from rest_framework.serializers import ModelSerializer, Serializer
from dishes.models import Dishes


class DishesSerializer(ModelSerializer):
    class Meta:
        model = Dishes
        fields = '__all__'
