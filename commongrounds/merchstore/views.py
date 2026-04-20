from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.list import ListView
from accounts.mixins import RoleRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


class ProductCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    required_role = "Market Seller"
    model = Product
    template_name = "product_create.html"
    fields = [
        "name",
        "product_type",
        "product_image",
        "description",
        "price",
        "stock",
        "status",
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    required_role = "Market Seller"
    model = Product
    template_name = "product_update.html"
    fields = [
        "name",
        "product_type",
        "product_image",
        "description",
        "price",
        "stock",
        "status",
    ]

    def form_valid(self, form):
        product = form.instance

        if product.stock == 0:
            product.status = "out_of_stock"
        else:
            product.status = "available"

        return super().form_valid(form)


@login_required
@role_required("Market Seller")
def cart_view(request):
    transactions = Transaction.objects.filter(buyer=request.user.profile)
    return render(request, "cart.html", {"transactions": transactions})


class TransactionsListView(DetailView):
    model = Product
    template_name = "transactions_list.html"


# Create your views here.
