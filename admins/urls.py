from django.urls import path
from admins.views import get_users, user_delete

urlpatterns = [
    path('users/', get_users, name='get_users'),
    path('user/delete/<int:pk>', user_delete, name='delete_user'),

]
