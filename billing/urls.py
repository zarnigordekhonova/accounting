
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (BrokerHistoryViewSet, FacilityHistoryViewSet, FacilitiesViewSet, BrokersViewSet,
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

urlpatterns = router.urls
