from django.views.generic import ListView, DetailView, TemplateView
from .models import Product

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'