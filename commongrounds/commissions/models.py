from django.db import models
from django.urls import reverse


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Commission(models.Model):
    class CommissionStatus(models.TextChoices):
        is_open = 'Open', 'Open'
        is_full = 'Full', 'Full'
        is_completed = 'Completed', 'Completed'
        is_discontinued = 'Discontinued', 'Discontinued'

    title = models.CharField(max_length=255)
    description = models.TextField()
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
    )
    maker = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        null=True,
    )
    people_required = models.PositiveIntegerField()
    status = models.CharField(
        choices=CommissionStatus.choices,
        default=CommissionStatus.is_open
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "created_on"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[str(self.id)])


class Job(models.Model):
    class JobStatus(models.TextChoices):
        is_open = 'Open', 'Open'
        is_full = 'Full', 'Full'

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        null=True,
        related_name="jobs"
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        choices=JobStatus.choices,
        default=JobStatus.is_open
    )

    class Meta:
        ordering = ["status", "-manpower_required", "role"]

    def __str__(self):
        return self.role
    
    def accepted_amount(self):
        return self.application.filter(status="Accepted").count()
    
    def job_full(self):
        return self.accepted_amount() >= self.manpower_required


class JobApplication(models.Model):
    class JobApplicationStatus(models.TextChoices):
        is_pending = 'Pending', 'Pending'
        is_accepted = 'Accepted', 'Accepted'
        is_rejected = 'Rejected', 'Rejected'

    applicant = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        null=True,
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        null=True,
        related_name="application"
    )
    status = models.CharField(
        choices=JobApplicationStatus.choices,
        default=JobApplicationStatus.is_pending
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["status", "-applied_on"]

    def __str__(self):
        return f"{self.applicant}"
