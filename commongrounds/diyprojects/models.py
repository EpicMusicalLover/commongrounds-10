from django.db import models
from django.urls import reverse

from accounts.models import Profile


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("diyprojects:project_detail", args=[str(self.pk)])


class Favorite(models.Model):
    STATUS_CHOICES = [
        ("Backlog", "Backlog"),
        ("To-Do", "To-Do"),
        ("Done", "Done"),
    ]
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="favorites"
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_favorited = models.DateField(auto_now_add=True)
    project_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Backlog"
    )

    def __str__(self):
        return f"{self.profile.display_name} favorited {self.project.title}"


class ProjectReview(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(
        upload_to="project_reviews/", blank=True, null=True)

    def __str__(self):
        return (
            f"Review by {self.reviewer.display_name} "
            f"on {self.project.title}"
        )


class ProjectRating(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="ratings"
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.score}/10 by {self.profile.display_name}"
