from django.urls import path, re_path
from user.views import user_create, login_user_token, get_current_user, user_update, CategoriesView, ProductsView

urlpatterns = [
    path('create/', user_create, name='user_create'),
    path('login/', login_user_token, name='user_login'),
    path('update/', user_update, name='user_update'),
    # path('login/', user_login, name='user_login'),
    # path('sms/verification/', sms_verification, name='sms_verification'),
    path('current/', get_current_user, name='current_user'),


    path('categories/', CategoriesView.as_view(), name='categories'),

    path('products/<int:category_id>/', ProductsView.as_view(), name='products'),
    re_path(r'^products/(?:(?P<category_id>\d+)/)?$', ProductsView.as_view(), name='products'),
]
