from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from admins.schemas import get_users_schema, user_delete_schema
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from utils.chack_auth import permission
from utils.pagination import paginate
from utils.responses import success


@get_users_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission(["admin"])
def get_users(request):
    role = request.query_params.get('role')
    users = CustomUser.objects.filter(is_active=True)
    if role:
        users = users.filter(role=role)
    return paginate(users.all(), CustomUserSerializer, request)


@user_delete_schema
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@permission(["admin"])
def user_delete(request, pk: int):
    user = get_object_or_404(CustomUser, id=pk)
    user.delete()
    return success
