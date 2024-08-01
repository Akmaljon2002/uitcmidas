from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from user.serializers import CustomUserSerializer
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