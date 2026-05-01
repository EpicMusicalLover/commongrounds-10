from django.views.generic import DetailView, CreateView, UpdateView, ListView
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Transaction, Product, ProductType
from .forms import TransactionForm


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TransactionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.get_object().owner == request.user.profile:
                return redirect("merchstore:product-detail", pk=self.get_object().pk)
        if TransactionForm(request.POST).is_valid():
            if not request.user.is_authenticated:
                return redirect("login")
            transaction = TransactionForm(request.POST).save(commit=False)
            transaction.product = self.get_object()
            transaction.buyer = request.user.profile
            transaction.status = "On cart"
            transaction.save()
            self.get_object().stock -= transaction.amount
            self.get_object().save()

            return redirect("merchstore:cart")

        return self.get(request, *args, **kwargs)


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
        if form.instance.stock == 0:
            form.instance.status = "out_of_stock"
        else:
            form.instance.status = "available"

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
