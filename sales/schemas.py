from drf_spectacular.utils import extend_schema
from sellers.serializers import CategorySerializer

# get_categories_schema = extend_schema(
#     summary="Get Categories",
#     responses={200: CategorySerializer(many=True),
#                401: {"description": "The operation wasn't completed successfully",
#                      "example": {'detail': 'Authentication credentials were not provided.'}},
#                403: {"description": "The operation wasn't completed successfully",
#                      "example": {'detail': "You don't have permission to perform this action."}},
#                }
# )