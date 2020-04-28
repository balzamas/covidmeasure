from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'measures', views.MeasureViewSet)
router.register(r'countries', views.CountryViewSet)
router.register(r'measuretypes', views.MeasureTypeViewSet)
router.register(r'measurecatgories', views.MeasureCategoryViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]
