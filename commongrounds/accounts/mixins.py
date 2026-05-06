from django.core.exceptions import PermissionDenied


class RoleRequiredMixin:
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())

        profile = request.user.profile
        if profile.role != self.required_role:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
