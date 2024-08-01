from drf_spectacular.utils import extend_schema, OpenApiParameter
from dishes.serializers import DishesSerializer

get_dishes_schema = extend_schema(
    summary="Get dishes",
    request=None,
    responses=DishesSerializer(many=True)
)
