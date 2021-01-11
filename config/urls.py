from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers
from measuremeterdata.views import view_deaths, view_deaths_ch,views_belgium, views_ranking_ch, views_ranking_int, viewsets, view_madlaina, view_measures_ch
from riskcalc import views as risk_views
from config import views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import JavaScriptCatalog
from django.conf.urls import url
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r'measures', viewsets.MeasureViewSet)

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('measuremeter',),  # my app name
}

urlpatterns = [
    path("", views.international, name="home"),
    path('openapi', get_schema_view(
                      title="Covidlaws",
                      description="API for all things …",
                      version="1.0.0"
                  ), name='openapi-schema'),
    path('ranking_europe/', views_ranking_int.ranking_europe, name='ranking_europe'),
    path('ranking_world/', views_ranking_int.ranking_world, name='ranking_world'),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
                      "barrace/", TemplateView.as_view(template_name="pages/barchart.html"), name="BarChartRace"
                  ),
    path(
        "euromap/", TemplateView.as_view(template_name="pages/euromap.html"), name="EuroMap"
      ),
    path('euromap/<str:measure_id>/', views.render_euromap, name='item'),
    path(
    "timeline/", TemplateView.as_view(template_name="pages/timeline.html"), name="Timeline"
                  ),
    path('timeline/<str:country_name>/', views.render_timeline, name='item'),
    path("compare/", TemplateView.as_view(template_name="pages/compare.html"), name="Compare"
                       ),
    path("compare/<str:country_name>/", views.render_compare, name="item"
                  ),
    path(
    "about/", TemplateView.as_view(template_name="pages/about.html"), name="About"
                  ),
    path('deaths/', view_deaths.country_deaths, name='deaths'),

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
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

                             )

urlpatterns += i18n_patterns(
    path(
        "madlaina/", view_madlaina.hallo_welt, name="Madlaina"
    ),
    path(
        "belrisk/", risk_views.belgium_risk, name="Bel Riskmap"
    ),
    path('deaths_ch/', view_deaths_ch.canton_deaths, name='deaths_ch'),
    path('measures_ch/', view_measures_ch.measures_ch, name='measures_ch'),
    path(
        "districts/", TemplateView.as_view(template_name="pages/district.html"), name="CH districts"
    ),
    path(
        "districts7/", TemplateView.as_view(template_name="pages/district7.html"), name="CH districts"
    ),
    path('ranking7/', views_ranking_ch.ranking7, name='ranking7'),
    path('ranking7all/', views_ranking_ch.ranking7_all, name='ranking7_all'),
    path('ranking14/', views_ranking_ch.ranking14, name='ranking14'),
    path('ranking14all/', views_ranking_ch.ranking14_all, name='ranking14_all'),
    path(
        "cantons/", TemplateView.as_view(template_name="pages/canton.html"), name="CH measures"
    ),
    path("cantons/<str:options>/", views.render_cantons, name="item"
         ),
    path(
        "ch/", views_ranking_ch.ch, name="CH Main"
    ),
    path(
        "chmaps/", TemplateView.as_view(template_name="pages/chmaps.html"), name="CH Maps"
    ),
    path(
        "chrisk/", TemplateView.as_view(template_name="pages/chrisk.html"), name="CH Riskmap"
    ),
)

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
