from django.urls import path
from sellers.views import SellerCategoriesView, SellerProductsView, SellerCreateProductView, SellerProductDetailView, \
    SellerSalesView, SellerSaleDetailView

urlpatterns = [
    path('categories/', SellerCategoriesView.as_view(), name='get_categories'),

    path('sales/', SellerSalesView.as_view(), name='get_sales'),
    path('sale/<int:pk>/', SellerSaleDetailView.as_view(), name='get_sale'),

    path('products/<int:category_id>/', SellerProductsView.as_view(), name='products_seller'),
    path('product/<int:pk>/', SellerProductDetailView.as_view(), name='product_seller'),
    path('products/create/', SellerCreateProductView.as_view(), name='products_create_seller'),

]