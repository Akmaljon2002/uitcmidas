from drf_spectacular.utils import extend_schema
from user.serializers import CustomUserSerializer, CreateUserResponseSerializer, \
    CustomUserTokenSerializer, LoginResponseSerializer, ErrorValSer, UserCategorySerializer, UserProductSerializer, \
    SaleCreateSerializer, ProductCreateSaleSerializer, ProductSaleSerializer, ProductUpdateSaleSerializer, \
    SalesSerializer
from utils.responses import response_schema

create_custom_user_schema = extend_schema(
    summary="Create new user",
    request=CustomUserSerializer,
    responses={
        201: CreateUserResponseSerializer,
        400: ErrorValSer(),
    }
)

login_custom_user_schema = extend_schema(
    summary="Login current user",
    request=CustomUserTokenSerializer,
    responses={200: LoginResponseSerializer,
               404: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'User not found!'}}
               }
)

get_current_user_schema = extend_schema(
    summary="Get current user",
    responses={200: CustomUserSerializer,
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}}
               }
)

user_update_schema = extend_schema(
    summary="User update",
    request=CustomUserSerializer,
    responses={200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}}
               })

get_user_categories_schema = extend_schema(
    summary="Get Categories",
    responses={200: UserCategorySerializer(many=True)}
)

get_user_products_schema = extend_schema(
    summary="Get Products",
    responses={200: UserProductSerializer(many=True)}
)

create_sale_schema = extend_schema(
    summary="Create new sale",
    request=SaleCreateSerializer,
    responses={
        200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
        400: ErrorValSer(),
        401: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'Authentication credentials were not provided.'}},
        404: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'User not found!'}}
    }
)

create_cart_schema = extend_schema(
    summary="Create new cart",
    request=ProductCreateSaleSerializer(),
    responses={
        200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
        400: ErrorValSer(),
        401: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'Authentication credentials were not provided.'}}
    }
)

update_cart_schema = extend_schema(
    summary="Update new cart",
    request=ProductUpdateSaleSerializer(),
    responses={
        200: {"description": "The operation was completed successfully", "example": {"detail": "Success!"}},
        400: ErrorValSer(),
        401: {"description": "The operation wasn't completed successfully",
              "example": {'detail': 'Authentication credentials were not provided.'}},
        403: {"description": "The operation wasn't completed successfully",
              "example": {'detail': "You don't have permission to perform this action."}},
        404: {"description": "The operation wasn't completed successfully",
              "example": {"detail": "No ProductSale matches the given query."}},
    }
)

get_carts_schema = extend_schema(
    summary="Get Carts",
    responses={200: ProductSaleSerializer(many=True),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               }
)

get_cart_schema = extend_schema(
    summary="Get Cart",
    responses={200: ProductSaleSerializer,
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               404: {"description": "The operation wasn't completed successfully",
                     "example": {"detail": "No ProductSale matches the given query."}},
               }
)

get_sales_schema = extend_schema(
    summary="Get sales",
    responses={200: SalesSerializer(many=True),
               401: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'Authentication credentials were not provided.'}},
               403: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': "You don't have permission to perform this action."}},
               }
)
