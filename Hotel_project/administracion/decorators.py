from django.shortcuts import redirect
from functools import wraps

def rol_requerido(*roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if not request.user.rol:
                return redirect("apps_home")

            if request.user.rol.nombre not in roles_permitidos:
                return redirect("apps_home")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator