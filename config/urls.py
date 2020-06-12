from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers
from measuremeterdata.views import MeasureViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'measures', MeasureViewSet)

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "euromap/", TemplateView.as_view(template_name="pages/euromap.html"), name="EuroMap"
      ),
    path('euromap/<str:measure_id>/', views.render_euromap, name='item'),
    path(
    "timeline/", TemplateView.as_view(template_name="pages/timeline.html"), name="Timeline"
                  ),
    path('timeline/<str:country_name>/', views.render_timeline, name='item'),
    path(
    "about/", TemplateView.as_view(template_name="pages/about.html"), name="About"
                  ),
    path(
    "country/", TemplateView.as_view(template_name="pages/country.html"), name="Country"
                  ),
                  path(
                      "test/", TemplateView.as_view(template_name="pages/test.html"), name="Test"
                  ),
    path('country/<str:country_name>/',views.render_country, name='item'),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("measuremeter.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path('measuremeterdata/', include('measuremeterdata.urls')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
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
