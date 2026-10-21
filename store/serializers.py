from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Brand, Product, ProductImage,
    CartItem, Review, BlogPost, UserProfile,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'icon', 'description']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'old_price', 'image',
            'category', 'brand', 'rating', 'review_count', 'stock',
            'is_featured', 'is_new', 'is_bestseller', 'is_deal',
            'deal_percentage', 'created_at',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'specifications',
            'price', 'old_price', 'image', 'category', 'brand',
            'rating', 'review_count', 'stock', 'is_featured', 'is_new',
            'is_bestseller', 'is_deal', 'deal_percentage',
            'images', 'reviews', 'created_at', 'updated_at',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    """Read serializer — returns nested product info."""
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'added_at']


class CartItemCreateSerializer(serializers.ModelSerializer):
    """Write serializer — accepts product id + quantity."""

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'image', 'excerpt',
            'content', 'category', 'author', 'created_at',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'profile']


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'specifications',
            'price', 'old_price', 'image', 'category', 'brand',
            'rating', 'review_count', 'stock', 'is_featured', 'is_new',
            'is_bestseller', 'is_deal', 'deal_percentage',
        ]
        extra_kwargs = {
            'slug': {'required': False},
        }

    def create(self, validated_data):
        if not validated_data.get('slug'):
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(validated_data['name']) or 'product'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            validated_data['slug'] = slug
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        # Create an empty profile for the new user
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
