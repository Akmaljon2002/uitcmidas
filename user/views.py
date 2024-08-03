from datetime import timedelta
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from sales.models import ProductSale, Sale
from sellers.models import Category, Product
from user.schemas import create_custom_user_schema, login_custom_user_schema, get_current_user_schema, \
    user_update_schema, get_user_categories_schema, get_user_products_schema, create_sale_schema, create_cart_schema, \
    get_carts_schema, get_cart_schema, update_cart_schema, get_sales_schema
from user.serializers import CustomUserSerializer, UserCategorySerializer, UserProductSerializer, SaleCreateSerializer, \
    ProductSaleSerializer, ProductCreateSaleSerializer, ProductUpdateSaleSerializer, SalesSerializer
from utils.chack_auth import IPThrottle, permission, RolePermission
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from utils.pagination import paginate
from utils.responses import success


def generate_access_token(user):
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=timedelta(days=365))
    return str(token)


class ClientBaseAuthView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]
    roles = ["client"]


@create_custom_user_schema
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
@transaction.atomic()
def user_create(request):
    serializer = CustomUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()
    user = authenticate(phone=serializer.validated_data['phone'],
                        password=serializer.validated_data['password'])
    refresh = RefreshToken.for_user(user)
    serialized_user = CustomUserSerializer(user).data
    return Response({'refresh': str(refresh),
                     'access': str(refresh.access_token),
                     'user': serialized_user}, status=201)


@login_custom_user_schema
@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([IPThrottle])
def login_user_token(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    user = authenticate(phone=phone, password=password)
    if user is None:
        return Response({'detail': 'User not found'}, status=404)
    refresh = RefreshToken.for_user(user)
    serialized_user = CustomUserSerializer(user).data
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': serialized_user})


@get_current_user_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=200)


@user_update_schema
@api_view(['PUT'])
def user_update(request):
    serializer = CustomUserSerializer(instance=request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


class CategoriesView(APIView):
    permission_classes = [AllowAny]

    @get_user_categories_schema
    def get(self, request):
        categories = Category.objects.all()
        serializer = UserCategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductsView(APIView):
    permission_classes = [AllowAny]

    @get_user_products_schema
    def get(self, request, category_id: int = None):
        products = Product.objects
        if category_id:
            products = products.filter(category__id=category_id)
        return paginate(products.all(), UserProductSerializer, request)


class AdminCartsView(ClientBaseAuthView):
    @get_carts_schema
    def get(self, request):
        carts = ProductSale.objects.filter(client=request.user).all()
        serializer = ProductSaleSerializer(carts, many=True)
        return Response(serializer.data)

    @create_cart_schema
    def post(self, request):
        serializer = ProductCreateSaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['count']:
            product = get_object_or_404(Product, id=serializer.validated_data['product'].id)
            cart = ProductSale.objects.filter(product=product, client=request.user).first()
            price = ((product.price * serializer.validated_data['count']) -
                     (product.price * serializer.validated_data['count'] * product.discount / 100))
            if cart:
                cart.count += 1
                cart.price = price
                cart.save()
            else:
                serializer.save(client=request.user, price=price)
        return success


class CartDetailView(ClientBaseAuthView):
    def _get_object(self, request, pk):
        return get_object_or_404(ProductSale, id=pk, client=request.user)

    @get_cart_schema
    def get(self, request, pk):
        category = self._get_object(pk)
        serializer = ProductSaleSerializer(category)
        return Response(serializer.data)

    @update_cart_schema
    def put(self, request, pk):
        cart = self._get_object(pk)
        if cart.count:
            serializer = ProductUpdateSaleSerializer(cart, data=request.data)
            serializer.is_valid(raise_exception=True)
            product = get_object_or_404(Product, id=cart.product.id)
            price = ((product.price * serializer.validated_data['count']) -
                     (product.price * serializer.validated_data['count'] * product.discount / 100))
            serializer.save(price=price)
        else:
            cart.delete()
        return success


@create_sale_schema
@api_view(['POST'])
@permission(['client'])
@throttle_classes([IPThrottle])
@transaction.atomic()
def sale_create(request):
    serializer = SaleCreateSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@get_sales_schema
@api_view(['GET'])
@permission(['client'])
@throttle_classes([IPThrottle])
@transaction.atomic()
def sales_get(request):
    sales = Sale.objects.filter(client=request.user).all()
    serializer = SalesSerializer(sales, many=True)
    return Response(serializer.data, 200)



