from django.urls import include, path
from .views import ProfileUpdateView

app_name = "accounts"

urlpatterns=[
    path("<str:username>/", ProfileUpdateView.as_view(), name="profile-update"),
    path("accounts/", include("django.contrib.auth.urls")),
]