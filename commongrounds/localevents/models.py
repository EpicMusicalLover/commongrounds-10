from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True,
    )
    organizer = models.ManyToManyField('accounts.Profile')
    event_image = models.ImageField(
        upload_to="images/",
        blank=False,
        null=False,
    )
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    event_capacity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=255,
        choices=[
            ("available", "Available"),
            ("full", "Full"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default='Available'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('localevents:event-detail', kwargs={'pk': self.pk})

class EventSignup(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="eventsignup"
    )

    user_registrant = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="eventsignup"
    )

    new_registrant = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

