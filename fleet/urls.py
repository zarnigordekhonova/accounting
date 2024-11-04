
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CompanyViewSet, DepartmentViewSet, UserStatusViewSet, UserListAPIView, UserUpdateView, UserRetrieveAPIView, UserProfileUpdateView,
                    DriverStatusViewSet, RecruiterViewSet, DriverTypeViewSet, DriverListCreateView, DriverRetrieveUpdateDestroyView, ActiveDriversView,
                    InActiveDriversView, MakesViewSet, TruckStatusesViewSet, ModelsViewSet, TrucksListCreateView, TrucksRetrieveUpdateDestroyView, ActiveTrucksListView,
                    TruckDriversListCreateView, TruckDriversRetrieveUpdateDeleteView, LessorCompanyView, VehicleTypeView, CarrierTypeView)

from decouple import config

router = DefaultRouter()
# users
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'user-statuses', UserStatusViewSet, basename='user-statuses')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'driver-statuses', DriverStatusViewSet, basename='driver-statuses')
router.register(r'recruiters', RecruiterViewSet, basename='recruiters')
router.register(r'driver-type', DriverTypeViewSet, basename='driver-type')
router.register(r'models', ModelsViewSet, basename='models')
router.register(r'truck-statuses', TruckStatusesViewSet, basename='truck-statuses')
router.register(r'makes', MakesViewSet)


urlpattern = [
    #users
    path('list/', UserListAPIView.as_view(), name='list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('user-profile/', UserRetrieveAPIView.as_view(), name='user-profile'),
    path('password-change/<int:pk>/', UserProfileUpdateView.as_view(), name='password-change'),
    path('drivers/', DriverListCreateView.as_view(), name='driver-list'),
    path('active-drivers/', ActiveDriversView.as_view(), name='active-drivers'),
    path('inactive-drivers/', InActiveDriversView.as_view(), name='inactive-drivers'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDestroyView.as_view(), name='driver-update'),
    path('trucks/', TrucksListCreateView.as_view(), name='trucks-list'),
    path('trucks/<int:pk>/', TrucksRetrieveUpdateDestroyView.as_view(), name='trucks-update'),
    path('truck-drivers/', TruckDriversListCreateView.as_view(), name='truck-drivers-list'),
    path('truck-drivers/<int:pk>/', TruckDriversRetrieveUpdateDeleteView.as_view(), name='truck-drivers-update'),
    path('active-trucks/', ActiveTrucksListView.as_view(), name='active-trucks'),
    path('vehicle-types/', VehicleTypeView.as_view(), name='vehicle-types-list'),
    path('lessor-companies/', LessorCompanyView.as_view(), name='lessor-company'),
    path('carrier-types/', CarrierTypeView.as_view(), name='carrier-types')
]

urlpatterns = router.urls + urlpattern
