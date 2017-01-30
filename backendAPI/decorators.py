from django.views.decorators.csrf import csrf_exempt

from .http import JsonError

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback


def header_required(view_func):
    """Decorator which ensures the header is correct"""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.content_type != 'application/json':
            return JsonError('Content-Type should be an application/json')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
