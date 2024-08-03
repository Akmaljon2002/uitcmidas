from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from sellers.serializers import CategorySerializer, ProductSerializer, SellerSalesSerializer
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

get_product_schema = extend_schema(
    summary="Get Product",
    responses={200: ProductSerializer,
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No Product matches the given query."}},
               }
)

update_product_schema = extend_schema(
    summary="Update Product",
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

delete_product_schema = extend_schema(
    summary="Delete Product",
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

get_sales_schema = extend_schema(
    summary="Get Sales",
    parameters=[
        OpenApiParameter(name='status', description='Sale status', required=False, type=OpenApiTypes.STR,
                         enum=['waiting', 'preparing', 'delivering', 'delivered'])
    ],
    responses={200: SellerSalesSerializer(many=True),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               }
)

get_sale_schema = extend_schema(
    summary="Get Sale",
    responses={200: SellerSalesSerializer,
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No Sale matches the given query."}},
               }
)

update_sale_schema = extend_schema(
    summary="Update Sale",
    parameters=[
        OpenApiParameter(name='status', description='Sale status', required=True, type=OpenApiTypes.STR,
                         enum=['waiting', 'preparing', 'delivering', 'delivered'])
    ],
    responses={
        200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
        400: ErrorValSer(),
        401: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'Authentication credentials were not provided.'}},
        403: {"description": "The operation wasn't completed successfully",
              "example": {'detail': "You don't have permission to perform this action."}},
        404: {"description": "The operation wasn't completed successfully",
              "example": {"detail": "No Sale matches the given query."}},
    }
)