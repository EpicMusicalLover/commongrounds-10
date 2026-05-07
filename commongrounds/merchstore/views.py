from django.views.generic import DetailView, CreateView, UpdateView, ListView
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from accounts.decorators import role_required
from .models import Transaction, Product
from .forms import TransactionForm
from .strategies import AuthenticatedPurchaseStrategy, GuestPurchaseStrategy


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["your_products"] = Product.objects.none()
        context["other_products"] = Product.objects.all()
        if user.is_authenticated and hasattr(user, "profile"):
            profile = getattr(user, "profile", None)
            context["your_products"] = Product.objects.filter(owner_id=profile.pk)
            context["other_products"] = Product.objects.exclude(owner_id=profile.pk)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TransactionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object
        user = request.user
        if (
            user.is_authenticated
            and product.owner == user.profile
        ):
            return redirect("merchstore:product-detail", pk=product.pk)
        form = TransactionForm(request.POST)
        if form.is_valid():
            if user.is_authenticated:
                strategy = AuthenticatedPurchaseStrategy()
            else:
                strategy = GuestPurchaseStrategy()
            return strategy.execute(request, product, form)
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
        user = self.request.user
        if user.is_authenticated:
            form.instance.owner = user.profile
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
            form.instance.status = "Out of Stock"
        else:
            form.instance.status = "Available"

        return super().form_valid(form)


@login_required
def cart_view(request):
    user = request.user
    transactions = Transaction.objects.filter(
        buyer=user.profile,
    )
    transactions_group = {}
    for t in transactions:
        owner = t.product.owner
        if owner not in transactions_group:
            transactions_group[owner] = []
        transactions_group[owner].append(t)

    return render(request, "cart.html", {"transactions": transactions_group})


class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions_list.html"
    context_object_name = "transactions"
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            product__owner=user.profile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = {}
        for t in context["transactions"]:
            buyer = t.buyer
            if buyer not in grouped:
                grouped[buyer] = []
            grouped[buyer].append(t)
        context["transactions_group"] = grouped
        return context


# Create your views here.
