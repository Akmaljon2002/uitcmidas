from drf_spectacular.utils import extend_schema
from user.serializers import CustomUserSerializer, CreateUserResponseSerializer, \
    CustomUserTokenSerializer, LoginResponseSerializer, ErrorValSer
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


