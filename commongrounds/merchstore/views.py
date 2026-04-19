from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

class ProductCreateView(DetailView):
    model = Product
    template_name = "product_create.html"


class ProductUpdateView(DetailView):
    model = Product
    template_name = "product_update.html"


class CartView(DetailView):
    model = Product
    template_name = "cart.html"


class TransactionsListView(DetailView):
    model = Product
    template_name = "transactions_list.html"


# Create your views here.
