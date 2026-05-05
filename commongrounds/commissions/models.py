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
        is_open = 'A', 'Open'
        is_full = 'B', 'Full'

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
        default = CommissionStatus.is_open
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.title


class Job(models.Model):
    class JobStatus(models.TextChoices):
        is_open = 'A', 'Open'
        is_full = 'B', 'Full'

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        choices=JobStatus.choices,
        default = JobStatus.is_open
    )

    class Meta:
        ordering = ["status", "-manpower_required", "role"]

    def __str__(self):
        return self.role


class JobApplication(models.Model):
    class JobApplicationStatus(models.TextChoices):
        is_pending = 'A', 'Pending'
        is_accepted = 'B', 'Accepted'
        is_rejected = 'C', 'Rejected'

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
    )
    applicant = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        null=True,
    )
    status = models.CharField(
        choices=JobApplicationStatus.choices,
        default = JobApplicationStatus.is_pending
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["status", "-applied_on"]
