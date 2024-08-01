from drf_spectacular.utils import extend_schema
from sellers.serializers import CategorySerializer, ProductSerializer
from user.serializers import ErrorValSer
from utils.pagination import PaginationGetSerializer

get_categories_schema = extend_schema(
    summary="Get Categories",
    responses={200: CategorySerializer(many=True),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               }
)

get_products_schema = extend_schema(
    summary="Get Products",
    responses={200: PaginationGetSerializer(result_serializer=ProductSerializer),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No Category matches the given query."}},
               }
)

create_product_schema = extend_schema(
    summary="Create Product",
    request=ProductSerializer,
    responses={
        200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
        400: ErrorValSer(),
        401: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'Authentication credentials were not provided.'}},
        403: {"description": "The operation wasn't completed successfully",
              "example": {'detail': "You don't have permission to perform this action."}},
        404: {"description": "The operation wasn't completed successfully",
              "example": {"detail": "No Category matches the given query."}},
    }
)