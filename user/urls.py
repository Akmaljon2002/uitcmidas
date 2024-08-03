from django.urls import path, re_path
from user.views import user_create, login_user_token, get_current_user, user_update, CategoriesView, ProductsView, \
    sale_create, AdminCartsView, CartDetailView, sales_get

urlpatterns = [
    path('create/', user_create, name='user_create'),
    # path('login/', login_user_token, name='user_login'),
    path('update/', user_update, name='user_update'),
    path('current/', get_current_user, name='current_user'),


    path('categories/', CategoriesView.as_view(), name='categories'),

    path('carts/', AdminCartsView.as_view(), name='carts'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart'),
    path('sale/create/', sale_create, name='sale_create'),
    path('sales/', sales_get, name='sales_get'),

    path('products/<int:category_id>/', ProductsView.as_view(), name='products'),
    re_path(r'^products/(?:(?P<category_id>\d+)/)?$', ProductsView.as_view(), name='products'),
]
