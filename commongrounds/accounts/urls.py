from django.urls import path
from .views import ProfileUpdateView, RegisterView

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "<str:username>/",
        ProfileUpdateView.as_view(),
        name="profile-update",
    ),
]
