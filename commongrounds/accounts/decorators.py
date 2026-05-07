from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            profile = request.user.profile
            if profile.role != required_role:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
