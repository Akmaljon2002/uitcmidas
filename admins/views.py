from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from admins.schemas import get_users_schema, user_delete_schema, get_categories_schema, create_category_schema, \
    get_category_schema, update_category_schema, delete_category_schema, get_admin_products_schema, \
    create_admin_product_schema, get_admin_product_schema, update_admin_product_schema, delete_admin_product_schema, \
    create_seller_schema, seller_update_schema
from admins.serializers import ProductAdminSerializer, SellerSerializer
from sellers.models import Category, Product
from sellers.serializers import CategorySerializer
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from utils.chack_auth import permission, RolePermission, IPThrottle
from utils.pagination import paginate
from utils.responses import success


class AdminBaseAuthView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]
    roles = ["admin"]


@get_users_schema
@api_view(['GET'])
@permission(["admin"])
def get_users(request):
    role = request.query_params.get('role')
    users = CustomUser.objects.filter(is_active=True)
    if role:
        users = users.filter(role=role)
    return paginate(users.all(), CustomUserSerializer, request)


@user_delete_schema
@api_view(['DELETE'])
@permission(["admin"])
def user_delete(request, pk: int):
    user = get_object_or_404(CustomUser, id=pk)
    user.delete()
    return success


@create_seller_schema
@api_view(['POST'])
@throttle_classes([IPThrottle])
@transaction.atomic()
@permission(["admin"])
def seller_create(request):
    serializer = SellerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(role="seller")
    return success


@seller_update_schema
@api_view(['PUT'])
def seller_update(request, pk:int):
    seller = get_object_or_404(CustomUser, id=pk)
    serializer = SellerSerializer(instance=seller, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


class AdminCategoriesView(AdminBaseAuthView):
    parser_classes = [MultiPartParser]

    @get_categories_schema
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @create_category_schema
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success


class AdminCategoryDetailView(AdminBaseAuthView):
    parser_classes = [MultiPartParser]

    def _get_object(self, pk):
        return get_object_or_404(Category, id=pk)

    @get_category_schema
    def get(self, request, pk):
        category = self._get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @update_category_schema
    def put(self, request, pk):
        category = self._get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success

    @delete_category_schema
    def delete(self, request, pk):
        category = self._get_object(pk)
        category.delete()
        return success


class AdminProductsView(AdminBaseAuthView):
    @get_admin_products_schema
    def get(self, request, category_id: int, seller_id: int):
        category = get_object_or_404(Category, id=category_id)
        seller = get_object_or_404(CustomUser, id=seller_id)

        products = Product.objects.filter(category=category, seller=seller).all()
        return paginate(products, ProductAdminSerializer, request)


class AdminCreateProductView(AdminBaseAuthView):
    parser_classes = [MultiPartParser]

    @create_admin_product_schema
    def post(self, request):
        serializer = ProductAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success


class AdminProductDetailView(AdminBaseAuthView):
    parser_classes = [MultiPartParser]

    def _get_object(self, pk):
        return get_object_or_404(Product, id=pk)

    @get_admin_product_schema
    def get(self, request, pk):
        product = self._get_object(pk)
        serializer = ProductAdminSerializer(product)
        return Response(serializer.data)

    @update_admin_product_schema
    def put(self, request, pk):
        product = self._get_object(pk)
        serializer = ProductAdminSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success

    @delete_admin_product_schema
    def delete(self, request, pk):
        category = self._get_object(pk)
        category.delete()
        return success




