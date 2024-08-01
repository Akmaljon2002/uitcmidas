from rest_framework.decorators import api_view
from rest_framework.response import Response
from dishes.models import Dishes
from dishes.schemas import get_dishes_schema
from dishes.serializers import DishesSerializer


@get_dishes_schema
@api_view(['GET'])
def get_dishes(request):
    categories = Dishes.objects.all().order_by('-id')
    serializer = DishesSerializer(categories, many=True)
    return Response(serializer.data, 200)
