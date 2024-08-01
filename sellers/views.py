from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sellers.models import Category, Product
from sellers.schemas import get_categories_schema, get_products_schema, create_product_schema
from sellers.serializers import CategorySerializer, ProductSerializer
from utils.chack_auth import permission, RolePermission
from utils.pagination import paginate
from utils.responses import success


class SellerBaseAuthView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]
    roles = ["seller"]


class SellerCategoriesView(SellerBaseAuthView):
    @get_categories_schema
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class SellerProductsView(SellerBaseAuthView):
    @get_products_schema
    def get(self, request, category_id: int):
        category = get_object_or_404(Category, id=category_id)

        products = Product.objects.filter(category=category, seller=request.user).all()
        return paginate(products, ProductSerializer, request)


class SellerCreateProductView(SellerBaseAuthView):
    parser_classes = [MultiPartParser]

    @create_product_schema
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)
        return success


# class SellerProductDetailView(SellerBaseAuthView):
#     parser_classes = [MultiPartParser]
#
#     def _get_object(self, pk):
#         return get_object_or_404(Product, id=pk)
#
#     @get_category_schema
#     def get(self, request, pk):
#         category = self._get_object(pk)
#         serializer = ProductSerializer(category)
#         return Response(serializer.data)
#
#     @update_category_schema
#     def put(self, request, pk):
#         category = self._get_object(pk)
#         serializer = ProductSerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return success
#
#     @delete_category_schema
#     def delete(self, request, pk):
#         category = self._get_object(pk)
#         category.delete()
#         return success
