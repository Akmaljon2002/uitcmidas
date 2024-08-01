from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from user.models import CustomUser
from user.schemas import create_custom_user_schema, login_custom_user_schema, get_current_user_schema
from user.serializers import CustomUserSerializer
from utils.chack_auth import IPThrottle
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction


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
    phone = serializer.validated_data['phone']
    user = CustomUser.objects.filter(phone=phone).first()

    if user:
        if user.is_active:
            return Response({'The user already exists!'}, 409)
        else:
            user.full_name = serializer.validated_data.get('full_name')
            user.email = serializer.validated_data.get('email')
            user.is_active = True
            user.save()

    else:
        serializer.save()
        user = authenticate(phone=serializer.validated_data['phone'],
                            password=serializer.validated_data['password'])
        refresh = RefreshToken.for_user(user)
        serialized_user = CustomUserSerializer(user).data
        return Response({'detail': 'Created successfully!',
                         'success': True,
                         'refresh': str(refresh),
                         'access': str(refresh.access_token),
                         'user': serialized_user}, status=201)
    return Response({'detail': 'Bad Request!',
                     'success': False,
                     'data': serializer.errors}, status=410)


@login_custom_user_schema
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
@transaction.atomic()
def login_user_token(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    user = authenticate(phone=phone, password=password)
    if user is None:
        return Response({'detail': 'User not found', 'success': False}, status=404)
    refresh = RefreshToken.for_user(user)
    serialized_user = CustomUserSerializer(user).data
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': serialized_user})


@get_current_user_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=200)
