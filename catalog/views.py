from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from django.urls import reverse_lazy
from .forms import ProductForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from catalog.services import get_products_by_category

# Create your views here.

@permission_required('catalog.can_unpublish_product')
def toggle_publication(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = not product.is_published
    product.save()
    return redirect('home')



class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = 'all_products_list'

        products = cache.get(cache_key)

        if not products:
            products = list(Product.objects.filter(is_published=True))

            cache.set(cache_key, products, 60)

        return products

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        product = form.save()
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.is_superuser

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        # 1. Получаем pk текущего товара из URL
        pk = self.kwargs.get('pk')

        # 2. Создаем уникальный ключ (например: 'product_1')
        cache_key = f'product_{pk}'

        # 3. Проверяем, есть ли этот товар в Redis
        product = cache.get(cache_key)

        # 4. Если в Redis пусто — вытаскиваем из БД и сохраняем в кеш на 60 секунд
        if not product:
            product = super().get_object(queryset)
            cache.set(cache_key, product, 60)

        return product

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        is_owner = self.request.user == product.owner
        is_moderator = self.request.user.has_perm('catalog.delete_product')
        return is_owner or is_moderator or self.request.user.is_superuser

class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'


def category_products_view(request, pk):
    # Получаем саму категорию, чтобы вывести её название в заголовке
    category = get_object_or_404(Category, pk=pk)

    # Вызываем нашу сервисную функцию, которая сама разберется с Redis
    products = get_products_by_category(category.pk)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_products.html', context)