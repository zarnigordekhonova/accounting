from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (DispatcherListViewSet, UsersByCompanyView, DriverByCompanyView)


router = DefaultRouter()
router.register(r'dispatcher-list', DispatcherListViewSet, basename='dispatcher-list')

urlpattern = [
    #dispatch
    path('list-driver/', DriverByCompanyView.as_view(), name='list-driver'),
    path('list-users/', UsersByCompanyView.as_view(), name='list-users'),
]


urlpatterns = router.urls + urlpattern
