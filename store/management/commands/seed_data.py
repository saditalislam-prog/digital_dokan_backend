"""
Management command to seed the Digital Dokan database with sample data with high quality realistic images.
Usage: py manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import (
    Category, Brand, Product, ProductImage,
    Review, BlogPost, UserProfile,
)

# Curated High-Definition Technology Photography
REAL_CATEGORY_IMAGES = {
    'smartphones': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=400&auto=format&fit=crop&q=80',
    'tablets': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&auto=format&fit=crop&q=80',
    'laptops': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&auto=format&fit=crop&q=80',
    'smartwatches': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&auto=format&fit=crop&q=80',
    'accessories': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400&auto=format&fit=crop&q=80',
    'gaming': 'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=400&auto=format&fit=crop&q=80',
}

REAL_BRAND_LOGOS = {
    'apple': '/brands/apple.png',
    'samsung': '/brands/samsung.png',
    'google': '/brands/google.png',
    'oneplus': '/brands/oneplus.png',
    'xiaomi': '/brands/xiaomi.png',
    'oppo': '/brands/oppo.png',
    'sony': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg',
    'microsoft': 'https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg',
}

REAL_PRODUCT_IMAGES = {
    'iphone-16-pro-max': [
        'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&auto=format&fit=crop&q=80',
    ],
    'samsung-galaxy-s24-ultra': [
        'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&auto=format&fit=crop&q=80',
    ],
    'google-pixel-9-pro': [
        'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop&q=80',
    ],
    'oneplus-12': [
        'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&auto=format&fit=crop&q=80',
    ],
    'iphone-16-pro': [
        'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop&q=80',
    ],
    'samsung-galaxy-z-fold-5': [
        'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop&q=80',
    ],
    'google-pixel-9': [
        'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80',
    ],
    'oneplus-nord-4': [
        'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&auto=format&fit=crop&q=80',
    ],
    'ipad-pro-m4': [
        'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600&auto=format&fit=crop&q=80',
    ],
    'samsung-galaxy-tab-s9': [
        'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80',
    ],
    'macbook-air-m3': [
        'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80',
    ],
    'samsung-galaxy-book4': [
        'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80',
    ],
    'apple-watch-ultra-2': [
        'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80',
    ],
    'samsung-galaxy-watch-6': [
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop&q=80',
    ],
    'airpods-pro-2': [
        'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80',
    ],
    'samsung-galaxy-buds-fe': [
        'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=600&auto=format&fit=crop&q=80',
    ],
    'ps5-dualsense-controller': [
        'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1605901309584-818e25960a8f?w=600&auto=format&fit=crop&q=80',
    ],
    'xbox-elite-controller': [
        'https://images.unsplash.com/photo-1605901309584-818e25960a8f?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=600&auto=format&fit=crop&q=80',
    ],
    'xiaomi-14-ultra': [
        'https://images.unsplash.com/photo-1533228876829-65c94e7b5025?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=600&auto=format&fit=crop&q=80',
    ],
    'oppo-find-x7-ultra': [
        'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1533228876829-65c94e7b5025?w=600&auto=format&fit=crop&q=80',
    ],
    'iphone-16': [
        'https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop&q=80',
    ],
    'xiaomi-pad-6': [
        'https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600&auto=format&fit=crop&q=80',
    ],
    'google-pixel-watch-2': [
        'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80',
    ],
    'oneplus-watch-2': [
        'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80',
    ],
}


class Command(BaseCommand):
    help = 'Seed the database with sample Digital Dokan data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with authentic images...')

        # Superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@digitaldokan.com',
                password='admin123',
            )
            UserProfile.objects.get_or_create(user=admin_user)
            self.stdout.write(self.style.SUCCESS('  Created superuser: admin / admin123'))
        else:
            admin_user = User.objects.get(username='admin')

        # Update categories with real photos
        categories_data = [
            {'name': 'Smartphones', 'slug': 'smartphones', 'description': 'Latest smartphones from top brands'},
            {'name': 'Tablets', 'slug': 'tablets', 'description': 'Tablets for work, creativity and play'},
            {'name': 'Laptops', 'slug': 'laptops', 'description': 'Powerful laptops for creators and professionals'},
            {'name': 'Smartwatches', 'slug': 'smartwatches', 'description': 'Stay connected and track fitness on your wrist'},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Essential accessories and charging gear'},
            {'name': 'Gaming', 'slug': 'gaming', 'description': 'Next-gen gaming gear and controllers'},
        ]
        categories = {}
        for cat in categories_data:
            img = REAL_CATEGORY_IMAGES.get(cat['slug'], '')
            obj, _ = Category.objects.update_or_create(
                slug=cat['slug'],
                defaults={
                    'name': cat['name'],
                    'image': img,
                    'description': cat['description'],
                },
            )
            categories[cat['slug']] = obj

        self.stdout.write(self.style.SUCCESS(f'  Updated {len(categories)} categories with real photos'))

        # Update brands with SVG logos
        brands_data = [
            {'name': 'Apple', 'slug': 'apple'},
            {'name': 'Samsung', 'slug': 'samsung'},
            {'name': 'Google', 'slug': 'google'},
            {'name': 'OnePlus', 'slug': 'oneplus'},
            {'name': 'Xiaomi', 'slug': 'xiaomi'},
            {'name': 'Oppo', 'slug': 'oppo'},
            {'name': 'Sony', 'slug': 'sony'},
            {'name': 'Microsoft', 'slug': 'microsoft'},
        ]
        brands = {}
        for br in brands_data:
            logo = REAL_BRAND_LOGOS.get(br['slug'], '')
            obj, _ = Brand.objects.update_or_create(
                slug=br['slug'],
                defaults={
                    'name': br['name'],
                    'logo': logo,
                },
            )
            brands[br['slug']] = obj

        self.stdout.write(self.style.SUCCESS(f'  Updated {len(brands)} brands with SVG logos'))

        # Update products with realistic images
        for slug, img_list in REAL_PRODUCT_IMAGES.items():
            primary_img = img_list[0]
            try:
                prod = Product.objects.get(slug=slug)
                prod.image = primary_img
                prod.save()

                # Update gallery images
                ProductImage.objects.filter(product=prod).delete()
                for idx, img_url in enumerate(img_list):
                    ProductImage.objects.create(
                        product=prod,
                        image=img_url,
                        is_primary=(idx == 0),
                    )
            except Product.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('  Updated all products with real high-resolution images!'))

        # Seed 6 Authentic Blog Posts
        blogs_data = [
            {
                'title': 'iPhone 16 vs Samsung Galaxy S24: Complete Comparison',
                'slug': 'iphone-16-vs-samsung-galaxy-s24-complete-comparison',
                'category': 'Review',
                'image': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=800&auto=format&fit=crop&q=80',
                'excerpt': 'A detailed head-to-head comparison of the two most popular flagship smartphones of 2024 and 2025.',
                'content': 'Comprehensive camera, battery, display and processing comparison.',
            },
            {
                'title': 'Must Have Accessories for Your Phone',
                'slug': 'must-have-accessories-for-your-phone',
                'category': 'Guide',
                'image': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&auto=format&fit=crop&q=80',
                'excerpt': 'Enhance your smartphone experience with these essential accessories that every phone owner should consider.',
                'content': 'GaN fast chargers, ANC earbuds, magnetic mounts and 9H tempered glass.',
            },
            {
                'title': 'Top 5 Upcoming Smartphones in 2025',
                'slug': 'top-5-upcoming-smartphones-in-2025',
                'category': 'Tech News',
                'image': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80',
                'excerpt': 'Get ready for these exciting smartphone launches in 2025. From foldables to AI-powered devices.',
                'content': 'Detailed look at Galaxy S25, iPhone 17 Air, Pixel 10 and OnePlus 13.',
            },
            {
                'title': 'How to Choose the Right Smartphone for Your Needs in 2024',
                'slug': 'how-to-choose-the-right-smartphone-for-your-needs-in-2024',
                'category': 'Tips',
                'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80',
                'excerpt': 'A comprehensive buyer guide helping you balance processor power, camera versatility, and battery longevity.',
                'content': 'Everything you need to know about specs, battery stamina, storage tiers and OS ecosystems.',
            },
            {
                'title': 'The Rise of Foldable Phones: Is 2025 the Right Time to Buy?',
                'slug': 'the-rise-of-foldable-phones-2025',
                'category': 'Tech News',
                'image': 'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=800&auto=format&fit=crop&q=80',
                'excerpt': 'Foldable and flip devices are maturing with zero gap hinges, water resistance, and crease-free displays. Here is what you need to know.',
                'content': 'Analysis of modern hinge technology, durability milestones and tablet multitasking workflows.',
            },
            {
                'title': 'Top Battery Optimization Tips to Extend Smartphone Lifespan',
                'slug': 'battery-optimization-tips-smartphone-lifespan',
                'category': 'Tips',
                'image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80',
                'excerpt': 'Simple battery health habits to keep your lithium-ion battery healthy for over 3 to 4 years without degradation.',
                'content': 'Practical guide to heat reduction, 80% charge limits, overnight habits and certified adapters.',
            },
        ]
        for b in blogs_data:
            BlogPost.objects.update_or_create(
                slug=b['slug'],
                defaults={
                    'title': b['title'],
                    'category': b['category'],
                    'image': b['image'],
                    'excerpt': b['excerpt'],
                    'content': b['content'],
                    'author': admin_user,
                },
            )
        self.stdout.write(self.style.SUCCESS(f'  Updated {len(blogs_data)} blog posts with authentic photography!'))
