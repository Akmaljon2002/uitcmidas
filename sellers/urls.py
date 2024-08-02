from django.urls import path
from sellers.views import SellerCategoriesView, SellerProductsView, SellerCreateProductView, SellerProductDetailView

urlpatterns = [
    path('categories/', SellerCategoriesView.as_view(), name='get_categories'),
    path('products/<int:category_id>/', SellerProductsView.as_view(), name='products_seller'),
    path('product/<int:pk>/', SellerProductDetailView.as_view(), name='product_seller'),
    path('products/create/', SellerCreateProductView.as_view(), name='products_create_seller'),

]