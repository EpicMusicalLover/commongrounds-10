from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.urls import reverse


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
    )
    owner = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        null=True,
    )
    product_image = models.ImageField(
        upload_to="images/",
        blank=False,
        null=False,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.IntegerField(
        validators = [MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=255,
        choices=[
            ("available", "Available"),
            ("on_sale", "On sale"),
            ("out_of_stock", "Out of stock"),
        ],
        default="available",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("merchstore:product-detail", kwargs={"pk": self.pk})


class Transaction(models.Model):
    buyer = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
    )
    amount = models.IntegerField(
        validators = [MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=255,
        choices=[
            ("on_cart", "On cart"),
            ("to_pay", "To Pay"),
            ("to_ship", "To Ship"),
            ("to_receive", "To Receive"),
            ("delivered", "Delivered"),
        ],
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.amount}"


# Create your models here.
