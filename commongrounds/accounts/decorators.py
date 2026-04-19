from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .models import Profile

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                raise PermissionDenied
            if profile.role != required_role:
                raise PermissionDenied 
            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
#for committing