from drf_spectacular.utils import extend_schema, OpenApiParameter
from user.serializers import UserCreateSerializer, UserLoginSerializer, \
    UserGetCurrentSerializer, UserUpdateSerializer, CustomUserSerializer, CreateUserResponseSerializer, \
    ErrorResponseSerializer, CustomUserTokenSerializer, LoginResponseSerializer
from utils.responses import response_schema

create_custom_user_schema = extend_schema(
    summary="Create new user",
    request=CustomUserSerializer,
    responses={
        201: CreateUserResponseSerializer,
        400: ErrorResponseSerializer,
        409: {"description": "The operation wasn't completed successfully",
              "example": {'response': 'The user already exists!'}},
    }
)

login_custom_user_schema = extend_schema(
    summary="Login current user",
    request=CustomUserTokenSerializer,
    responses={200: LoginResponseSerializer,
               404: {"description": "The operation wasn't completed successfully",
                     "example": {'detail': 'User not found!',
                                 'success': False}}
               }
)

user_create_schema = extend_schema(
    summary="User create",
    request=UserCreateSerializer,
    responses={
        200: {"description": "The operation was completed successfully",
              "example": {'response': 'User created successfully'}},
        400: {"description": "The operation wasn't completed successfully",
              "example": {'response': 'The user already exists!'}},
        429: {"description": "The operation wasn't completed successfully",
              "example": {"detail": "Request was throttled. Expected available in (number) seconds."}},
    }
)

user_login_schema = extend_schema(
    summary="User login",
    request=UserLoginSerializer,
    responses={
        200: {"description": "The operation was completed successfully",
              "example": {'response': 'An SMS was sent, It is valid for 5 minutes'}},
        404: {"description": "The operation wasn't completed successfully",
              "example": {'response': 'CustomUser not found!'}},
        429: {"description": "The operation wasn't completed successfully",
              "example": {"detail": "Request was throttled. Expected available in (number) seconds."}},
    }
)


current_user_schema = extend_schema(
    summary="Get current user",
    responses=UserGetCurrentSerializer
)

user_update_schema = extend_schema(
    summary="User update",
    request=UserUpdateSerializer,
    responses=response_schema
)

user_delete_schema = extend_schema(
    summary="User delete",
    responses=response_schema
)
