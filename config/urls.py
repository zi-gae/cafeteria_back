from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework_jwt.views import obtain_jwt_token
from cafeteria import views


urlpatterns = [

    path("rest-auth/", include('rest_auth.urls')),
    path("rest-auth/registration/", include('rest_auth.registration.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("cafeteria.users.urls", namespace="users")),
    path("posts/", include("cafeteria.images.urls", namespace="images")),
    path("notifications/", include("cafeteria.notifications.urls", namespace="notifications")),
    path("accounts/", include("allauth.urls")),
    path("crawler/", include("cafeteria.crawler.urls")),

    path("", views.ReactAppView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
