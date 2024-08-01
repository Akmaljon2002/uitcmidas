from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from user.schemas import create_custom_user_schema, login_custom_user_schema, get_current_user_schema, \
    user_update_schema
from user.serializers import CustomUserSerializer
from utils.chack_auth import IPThrottle, permission
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from utils.responses import success


def generate_access_token(user):
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=timedelta(days=365))
    return str(token)


@create_custom_user_schema
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
@transaction.atomic()
def user_create(request):
    serializer = CustomUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()
    user = authenticate(phone=serializer.validated_data['phone'],
                        password=serializer.validated_data['password'])
    refresh = RefreshToken.for_user(user)
    serialized_user = CustomUserSerializer(user).data
    return Response({'refresh': str(refresh),
                     'access': str(refresh.access_token),
                     'user': serialized_user}, status=201)


@login_custom_user_schema
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
def login_user_token(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    user = authenticate(phone=phone, password=password)
    if user is None:
        return Response({'detail': 'User not found'}, status=404)
    refresh = RefreshToken.for_user(user)
    serialized_user = CustomUserSerializer(user).data
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': serialized_user})


@get_current_user_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=200)


@user_update_schema
@api_view(['PUT'])
def user_update(request):
    serializer = CustomUserSerializer(instance=request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


