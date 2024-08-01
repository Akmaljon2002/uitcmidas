from datetime import datetime, timedelta
from functools import wraps

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication


class IPThrottle(UserRateThrottle):
    rate = '5/min'


def allowed_only_admin():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator


def permission(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission to perform this action.'}, 403)
        return wrapper_func
    return decorator


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in view.roles:
            return True
        else:
            raise PermissionDenied("You don\'t have permission to perform this action.")

