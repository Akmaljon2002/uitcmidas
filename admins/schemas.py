from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from admins.serializers import ProductAdminSerializer, SellerSerializer
from sellers.serializers import CategorySerializer
from user.serializers import CustomUserSerializer, ErrorValSer
from utils.pagination import PaginationGetSerializer

get_users_schema = extend_schema(
    summary="Get users",
    parameters=[
        OpenApiParameter(name='role', description='User Role', required=False, type=OpenApiTypes.STR,
                         enum=['seller', 'client', 'admin'])
    ],
    responses={200: PaginationGetSerializer(result_serializer=CustomUserSerializer),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               }
)

user_delete_schema = extend_schema(
    summary="User delete",
    responses={200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               })

get_categories_schema = extend_schema(
    summary="Get Categories",
    responses={200: CategorySerializer(many=True),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               }
)

get_category_schema = extend_schema(
    summary="Get Category",
    responses={200: CategorySerializer,
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No Category matches the given query."}},
               }
)

create_category_schema = extend_schema(
    summary="Create Category",
    request=CategorySerializer,
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

update_category_schema = extend_schema(
    summary="Update Category",
    request=CategorySerializer,
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

delete_category_schema = extend_schema(
    summary="Delete Category",
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

get_admin_products_schema = extend_schema(
    summary="Get Products",
    responses={200: PaginationGetSerializer(result_serializer=ProductAdminSerializer),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No Category matches the given query."}},
               }
)

create_admin_product_schema = extend_schema(
    summary="Create Product",
    request=ProductAdminSerializer,
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

get_admin_product_schema = extend_schema(
    summary="Get Product",
    responses={200: ProductAdminSerializer,
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No Product matches the given query."}},
               }
)

update_admin_product_schema = extend_schema(
    summary="Update Product",
    request=ProductAdminSerializer,
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

delete_admin_product_schema = extend_schema(
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

create_seller_schema = extend_schema(
    summary="Create new seller",
    request=SellerSerializer,
    responses={
        200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
        400: ErrorValSer(),
        401: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'Authentication credentials were not provided.'}},
        403: {"description": "The operation wasn't completed successfully",
              "example": {'detail': "You don't have permission to perform this action."}},
    }
)

seller_update_schema = extend_schema(
    summary="Seller update",
    request=SellerSerializer,
    responses={200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}}
})
