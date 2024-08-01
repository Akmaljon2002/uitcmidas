from datetime import timedelta

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from user.models import CustomUser
from user.schemas import user_create_schema, user_login_schema, \
    user_update_schema, user_delete_schema, create_custom_user_schema, login_custom_user_schema, get_current_user_schema
from user.serializers import UserCreateSerializer, UserLoginSerializer, \
    UserUpdateSerializer, CustomUserSerializer
from utils.chack_auth import IPThrottle
from rest_framework.permissions import AllowAny, IsAuthenticated
import aiohttp
import asyncio
from utils.responses import success
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
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone = serializer.validated_data['phone']
    user = CustomUser.objects.filter(phone=phone).first()

    if user:
        if user.is_active:
            return Response({'detail': 'The user already exists!'}, 409)
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
                     'data': serializer.errors}, status=400)


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


# @user_login_schema
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @throttle_classes([IPThrottle])
# def user_login(request):
#     serializer = UserLoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     phone = serializer.validated_data['phone']
#
#     CustomUser.objects.get(phone=phone, is_active=True)
#     return Response({'detail': 'An SMS was sent, It is valid for 5 minutes'}, 200)


# @sms_verification_schema
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @throttle_classes([IPThrottle])
# def sms_verification(request):
#     serializer = SmsVerificationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     phone = serializer.validated_data['phone']
#     code = serializer.validated_data['code']
#
#     if len(str(code)) != 6:
#         return Response({'detail': 'Verification code must be 6 digits long!'}, 422)
#
#     user = CustomUser.objects.get(phone=phone)
#
#     if phone == '911111111' and code == 111111:
#         token = generate_access_token(user)
#         return Response({'access_token': token}, 200)
#
#     verification_code = Redis.get(phone)
#     if not verification_code:
#         return Response({'detail': 'Code has been expired!'}, 400)
#     if code != int(verification_code):
#         return Response({'detail': 'The verification code is incorrect!'}, 400)
#     user.is_active = True
#     user.save()
#     token = generate_access_token(user)
#     return Response({'access_token': token}, 200)
#
#
# @current_user_schema
# @api_view(['GET'])
# def current_user(request):
#     serializer = UserGetCurrentSerializer(request.user)
#     return Response(serializer.data, 200)
#
#
# @user_update_schema
# @api_view(['PUT'])
# def user_update(request):
#     serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return success
#
#
# @user_delete_schema
# @api_view(['DELETE'])
# def user_delete(request):
#     request.user.delete()
#     return success
#
#
# @get_version
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_version(request):
#     device = request.query_params.get('device')
#     version = request.query_params.get('version')
#     version_data = get_object_or_404(Version, version=version, device=device)
#     serializer = VersionGetSerializer(version_data)
#     return Response(serializer.data, 200)
