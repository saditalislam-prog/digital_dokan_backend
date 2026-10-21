from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from .models import (
    Category, Brand, Product, ProductImage,
    CartItem, Review, BlogPost, UserProfile,
)
from .serializers import (
    CategorySerializer, BrandSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductWriteSerializer,
    CartItemSerializer, CartItemCreateSerializer,
    ReviewSerializer, BlogPostSerializer,
    UserSerializer, RegisterSerializer,
)


# ──────────────────────────────────────────────
# Auth Views
# ──────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })
    return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ──────────────────────────────────────────────
# Product Views
# ──────────────────────────────────────────────

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.select_related('category', 'brand').all()

        # Filters
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        search = self.request.query_params.get('search')
        is_featured = self.request.query_params.get('featured')
        is_new = self.request.query_params.get('new')
        is_bestseller = self.request.query_params.get('bestseller')
        is_deal = self.request.query_params.get('deal')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        sort = self.request.query_params.get('sort')

        if category:
            qs = qs.filter(category__slug=category)
        if brand:
            qs = qs.filter(brand__slug=brand)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        if is_featured:
            qs = qs.filter(is_featured=True)
        if is_new:
            qs = qs.filter(is_new=True)
        if is_bestseller:
            qs = qs.filter(is_bestseller=True)
        if is_deal:
            qs = qs.filter(is_deal=True)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)

        if sort == 'price_low':
            qs = qs.order_by('price')
        elif sort == 'price_high':
            qs = qs.order_by('-price')
        elif sort == 'rating':
            qs = qs.order_by('-rating')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')

        return qs


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related('category', 'brand').prefetch_related('images', 'reviews')
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'


# ──────────────────────────────────────────────
# Category Views
# ──────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ──────────────────────────────────────────────
# Brand Views
# ──────────────────────────────────────────────

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# ──────────────────────────────────────────────
# Cart Views
# ──────────────────────────────────────────────

class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related(
            'product', 'product__category', 'product__brand',
        )


class CartAddView(generics.CreateAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        # If the product is already in the cart, bump its quantity instead
        try:
            cart_item = CartItem.objects.get(
                user=self.request.user, product=product,
            )
            cart_item.quantity += serializer.validated_data.get('quantity', 1)
            cart_item.save()
        except CartItem.DoesNotExist:
            serializer.save(user=self.request.user)


class CartUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class CartDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def cart_clear(request):
    CartItem.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ──────────────────────────────────────────────
# Review Views
# ──────────────────────────────────────────────

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_slug = self.request.query_params.get('product')
        if product_slug:
            return Review.objects.filter(product__slug=product_slug)
        return Review.objects.all()[:10]


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ──────────────────────────────────────────────
# Blog Views
# ──────────────────────────────────────────────

class BlogListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer


class BlogDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'


# ──────────────────────────────────────────────
# Admin CRUD Views
# ──────────────────────────────────────────────

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class BrandCreateView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandDeleteView(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class BlogCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]


class BlogDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_stats(request):
    return Response({
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_brands': Brand.objects.count(),
        'total_blogs': BlogPost.objects.count(),
        'total_reviews': Review.objects.count(),
        'total_users': User.objects.count(),
    })

