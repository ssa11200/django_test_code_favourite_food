from django.shortcuts import redirect
from django.http import HttpResponse


def require_auth(message="authentication failed!", redirect_view=None):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:

                if redirect_view:

                    return redirect(redirect_view)

                return HttpResponse(message, status=400)

            return view_function(request, *args, **kwargs)

        return wrapper

    return decorator


def require_admin(message="Unauthorized!", redirect_view=None):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):

            if not request.user.is_superuser:

                if redirect_view:

                    return redirect(redirect_view)

                return HttpResponse(message, status=401)

            return view_function(request, *args, **kwargs)

        return wrapper

    return decorator