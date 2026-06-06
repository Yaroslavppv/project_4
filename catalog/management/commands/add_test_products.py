from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_list = [
            {'name': 'Электроника', 'description': 'Гаджеты и техника'},
            {'name': 'Одежда', 'description': 'Стильные вещи'},
        ]

        categories_for_create = []
        for cat_item in categories_list:
            categories_for_create.append(Category(**cat_item))

        Category.objects.bulk_create(categories_for_create)

        cat_electronics = Category.objects.get(name='Электроника')

        products_list = [
            {'name': 'iPhone 15', 'price': 90000, 'category': cat_electronics},
            {'name': 'MacBook Pro', 'price': 200000, 'category': cat_electronics},
        ]

        products_for_create = []
        for prod_item in products_list:
            products_for_create.append(Product(**prod_item))

        Product.objects.bulk_create(products_for_create)

        self.stdout.write(self.style.SUCCESS('База данных успешно очищена и заполнена тестовыми данными!'))