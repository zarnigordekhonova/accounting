
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (BrokerHistoryViewSet, FacilityHistoryViewSet, FacilitiesViewSet, BrokersViewSet, LoadStopsViewSet,
                    LoadsViewSet, LoadProcessesViewSet, StatusesViewSet, LoadHistoryViewSet, LoadFilesViewSet)

router = DefaultRouter()
router.register(r'broker-history', BrokerHistoryViewSet, basename='broker-history')
router.register(r'facility-history', FacilityHistoryViewSet, basename="facility-history")
router.register(r'facilities', FacilitiesViewSet, basename="facilities")
router.register(r'brokers', BrokersViewSet, basename="brokers")
router.register(r'loads', LoadsViewSet, basename="loads")
router.register(r'load-processes', LoadProcessesViewSet, basename="load-processes")
router.register(r'statuses', StatusesViewSet, basename="statuses")
router.register(r'load-history', LoadHistoryViewSet, basename="load-history")
router.register(r'load-files', LoadFilesViewSet, basename="load-files")
router.register(r'load-stops', LoadStopsViewSet, basename="load-stops")

urlpatterns = router.urls
