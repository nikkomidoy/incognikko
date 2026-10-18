from django.conf import settings

DJANGO_ADMIN_PREFIX = "/django-admin/"
ADMIN_PREFIXES = ("/admin/", DJANGO_ADMIN_PREFIX)


class AdminCSPMiddleware:
    """Swap in `SECURE_CSP_ADMIN` for the CMS and `SECURE_CSP_DJANGO_ADMIN` for the Django admin
    (Unfold); public pages keep the strict policy."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(ADMIN_PREFIXES) and not hasattr(response, "_csp_config"):
            if request.path.startswith(DJANGO_ADMIN_PREFIX):
                response._csp_config = settings.SECURE_CSP_DJANGO_ADMIN
            else:
                response._csp_config = settings.SECURE_CSP_ADMIN
        return response


def zeal_skip_admin(get_response):
    """Dev only: don't raise on N+1s inside Wagtail/Django admin internals."""
    from zeal import zeal_ignore

    def middleware(request):
        if request.path.startswith(ADMIN_PREFIXES):
            with zeal_ignore():
                return get_response(request)
        return get_response(request)

    return middleware
