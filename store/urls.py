from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', views.login_view),
    path('auth/profile/', views.profile_view),

    # Products
    path('products/', views.ProductListView.as_view()),
    path('products/create/', views.ProductCreateView.as_view()),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view()),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view()),
    path('products/<slug:slug>/', views.ProductDetailView.as_view()),

    # Categories
    path('categories/', views.CategoryListView.as_view()),
    path('categories/create/', views.CategoryCreateView.as_view()),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view()),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view()),

    # Brands
    path('brands/', views.BrandListView.as_view()),
    path('brands/create/', views.BrandCreateView.as_view()),
    path('brands/<int:pk>/update/', views.BrandUpdateView.as_view()),
    path('brands/<int:pk>/delete/', views.BrandDeleteView.as_view()),

    # Cart
    path('cart/', views.CartListView.as_view()),
    path('cart/add/', views.CartAddView.as_view()),
    path('cart/<int:pk>/update/', views.CartUpdateView.as_view()),
    path('cart/update/<int:pk>/', views.CartUpdateView.as_view()),
    path('cart/<int:pk>/delete/', views.CartDeleteView.as_view()),
    path('cart/remove/<int:pk>/', views.CartDeleteView.as_view()),
    path('cart/clear/', views.cart_clear),

    # Reviews
    path('reviews/', views.ReviewListView.as_view()),
    path('reviews/create/', views.ReviewCreateView.as_view()),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view()),

    # Blog
    path('blog/', views.BlogListView.as_view()),
    path('blog/create/', views.BlogCreateView.as_view()),
    path('blog/<int:pk>/update/', views.BlogUpdateView.as_view()),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view()),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view()),

    # Admin Dashboard Stats
    path('admin/stats/', views.admin_stats),
]
