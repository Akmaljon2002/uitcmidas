from django.urls import path
from user.views import user_create, login_user_token, get_current_user

urlpatterns = [
    path('create/', user_create, name='user_create'),
    path('login/', login_user_token, name='user_login'),
    # path('update/', user_update, name='user_update'),
    # path('delete/', user_delete, name='user_delete'),
    # path('login/', user_login, name='user_login'),
    # path('sms/verification/', sms_verification, name='sms_verification'),
    path('current/', get_current_user, name='current_user'),
]
