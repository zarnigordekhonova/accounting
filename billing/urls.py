
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (BrokerHistoryViewSet, FacilityHistoryViewSet, FacilitiesViewSet, BrokersViewSet, LoadStopsViewSet,
                    FacilityByIdAPIView, LoadsViewSet, LoadProcessesViewSet, StatusesViewSet, LoadHistoryViewSet,
                    LoadFilesViewSet, BrokerByIdAPIView, LoadByIdAPIView, BookedByListAPIView)

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

urlpattern = ([
    path('brokers/<int:pk>/history/', BrokerByIdAPIView.as_view(), name='brokerhistory-by-id'),
    path('facilities/<int:pk>/history/', FacilityByIdAPIView.as_view(), name='facilityhistory-by-id'),
    path('loads/<int:pk>/history/', LoadByIdAPIView.as_view(), name='loadhistory-by-id'),
    path('booked-by/', BookedByListAPIView.as_view(), name='booked-by-list')
])

urlpatterns = urlpattern + router.urls

