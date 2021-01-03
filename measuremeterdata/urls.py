from django.urls import include, path
from rest_framework import routers
from measuremeterdata.views import viewsets

router = routers.DefaultRouter()
router.register(r'measures', viewsets.MeasureViewSet)
router.register(r'oxfordmeasures', viewsets.OxfordMeasureViewSet)

router.register(r'measuresbymeasure', viewsets.MeasureByMeasureViewSet)
router.register(r'countries', viewsets.CountryWithMeasuresViewSet)
router.register(r'measuretypes', viewsets.MeasureTypeViewSet)
router.register(r'oxfordmeasuretypes', viewsets.OxfordMeasureTypeViewSet)

router.register(r'measurecatgories', viewsets.MeasureCategoryViewSet)
router.register(r'casesdeaths', viewsets.CasesDeathsViewSet)

router.register(r'chmeasures_intern', viewsets.CHMeasureViewSet)
router.register(r'chmeasuretypes_intern', viewsets.CHMeasureTypeViewSet)
router.register(r'chcantons', viewsets.CHCantonViewSet)
router.register(r'chcases', viewsets.CHCasesViewSet)
router.register(r'chmeasures', viewsets.CHMeasurePublicViewset)
router.register(r'chdeaths', viewsets.CHDeathsPublicViewset)
router.register(r'chmeasuretypes', viewsets.CHMeasureTypePublicViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),

]
