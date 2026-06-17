from django.core.cache import cache
from django.conf import settings
from catalog.models import Product


def get_products_by_category(category_id):
    """Возвращает список всех опубликованных продуктов в указанной категории с кешированием."""
    if not settings.CACHES:
        return Product.objects.filter(category_id=category_id, is_published=True)

    cache_key = f'category_{category_id}_products'

    products_list = cache.get(cache_key)

    if products_list is None:
        products_list = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(cache_key, products_list, 300)

    return products_list