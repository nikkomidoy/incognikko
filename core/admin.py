"""Re-theme third-party Django admin registrations with django-unfold."""

from importlib import import_module

from django.contrib import admin
from unfold.admin import ModelAdmin

# These apps come after `core` in INSTALLED_APPS, so load their admin modules now to have
# their registrations in place to wrap (autodiscover won't re-run an imported module).
for module in (
    "allauth.account.admin",
    "allauth.mfa.admin",
    "axes.admin",
    "django.contrib.sites.admin",
    "taggit.admin",
    "wagtail.documents.admin",
    "wagtail.images.admin",
):
    import_module(module)

for model, model_admin in list(admin.site._registry.items()):
    if isinstance(model_admin, ModelAdmin):
        continue
    base = type(model_admin)
    admin.site.unregister(model)
    if base is admin.ModelAdmin:
        admin.site.register(model, ModelAdmin)
    else:
        admin.site.register(model, type(base.__name__, (base, ModelAdmin), {}))  # pyright: ignore[reportGeneralTypeIssues]
