from django.urls import path
from admins.views import get_users, user_delete, AdminCategoriesView, AdminCategoryDetailView, AdminProductsView, \
    AdminCreateProductView, AdminProductDetailView

urlpatterns = [
    path('users/', get_users, name='get_users'),
    path('user/delete/<int:pk>', user_delete, name='delete_user'),

    path('categories/', AdminCategoriesView.as_view(), name='categories_admin'),
    path('category/<int:pk>/', AdminCategoryDetailView.as_view(), name='category_admin'),

    path('products/<int:category_id>/<int:seller_id>/', AdminProductsView.as_view(), name='products_admin'),
    path('product/<int:pk>/', AdminProductDetailView.as_view(), name='product_admin'),
    path('products/create/', AdminCreateProductView.as_view(), name='products_create_admin'),

]
