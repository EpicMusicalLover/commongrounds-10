from django.db import models


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Commission(models.Model):
    class CommissionStatus(models.TextChoices):
        isOpen = 'Open'
        isFull = 'Full'

    title = models.CharField(max_length=255)
    description = models.TextField()
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
    )
    maker = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        null=True,
    )
    people_required = models.PositiveIntegerField()
    status = models.CharField(
        choices=CommissionStatus.choices,
        default = CommissionStatus.isOpen
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.title
