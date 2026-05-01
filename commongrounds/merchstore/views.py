from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.list import ListView
from accounts.mixins import RoleRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Transaction, Product, ProductType
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "all_products"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["your_products"] = Product.objects.filter(owner=self.request.user.profile)
            context["other_products"] = Product.objects.exclude(owner=self.request.user.profile)
        else:
            context["other_products"] = Product.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


class ProductCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    required_role = "Market Seller"
    model = Product
    template_name = "product_create.html"
    fields = [
        "name",
        "product_image",
        "description",
        "price",
        "stock",
        "status",
    ]

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.instance.product_type = ProductType.objects.first()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    required_role = "Market Seller"
    model = Product
    template_name = "product_update.html"
    fields = [
        "name",
        "product_image",
        "description",
        "price",
        "stock",
        "status",
    ]

    def form_valid(self, form):
        product = form.instance
        form.instance.product_type = self.get_object().product_type

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
