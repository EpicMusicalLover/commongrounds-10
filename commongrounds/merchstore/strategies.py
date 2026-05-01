from django.shortcuts import redirect
from django.urls import reverse


class BaseTransactionStrategy:
    def execute(self, request, product, form):
        raise NotImplementedError


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction = form.save(commit=False)
        transaction.buyer = request.user.profile
        transaction.product = product
        transaction.status = "On cart"
        transaction.save()

        return redirect(reverse("merchstore:cart"))


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session["pending_transaction"] = {
            "product_id": product.id,
            "amount": form.cleaned_data["amount"],
        }

        return redirect("login")