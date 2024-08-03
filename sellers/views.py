from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from admins.schemas import delete_category_schema
from sales.models import Sale
from sellers.models import Category, Product
from sellers.schemas import get_categories_schema, get_products_schema, create_product_schema, get_product_schema, \
    update_product_schema, get_sales_schema, get_sale_schema, update_sale_schema
from sellers.serializers import CategorySerializer, ProductSerializer, SellerSalesSerializer
from user.models import CustomUser
from utils.chack_auth import RolePermission
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


class SellerProductDetailView(SellerBaseAuthView):
    parser_classes = [MultiPartParser]

    def _get_object(self, request, pk):
        return get_object_or_404(Product, id=pk, seller=request.user)

    @get_product_schema
    def get(self, request, pk):
        product = self._get_object(request, pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @update_product_schema
    def put(self, request, pk):
        product = self._get_object(request, pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success

    @delete_category_schema
    def delete(self, request, pk):
        category = self._get_object(request, pk)
        category.delete()
        return success


class SellerSalesView(SellerBaseAuthView):
    @get_sales_schema
    def get(self, request):
        status = request.query_params.get("status")
        sales = Sale.objects.filter(seller_id=request.user.id)
        if status:
            sales = sales.filter(status=status)
        serializer = SellerSalesSerializer(sales.all(), many=True)
        return Response(serializer.data)


class SellerSaleDetailView(SellerBaseAuthView):
    def _get_object(self, request, pk):
        return get_object_or_404(Sale, id=pk, seller_id=request.user.id)

    @get_sale_schema
    def get(self, request, pk):
        sale = self._get_object(request, pk)
        serializer = SellerSalesSerializer(sale)
        return Response(serializer.data)

    @update_sale_schema
    def put(self, request, pk):
        sale = self._get_object(request, pk)
        status = request.query_params.get("status")
        sale.status = status
        sale.save()
        return success

