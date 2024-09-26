from django.urls import path, include
from rest_framework import routers

from .views import (
    RegisterAPIView, UserProfileUpdateView, UserListAPIView, UserUpdateView, PasswordResetRequestView, PasswordResetView, UserRetrieveAPIView,
    BranchesViewSet, RolesViewSet, UserRolesView
)

router = routers.DefaultRouter()
router.register(r'branches', BranchesViewSet, basename='branches')
router.register(r'roles', RolesViewSet, basename='roles')
router.register(r'user-roles', UserRolesView, basename='user-roles')

urlpatterns = [
    path('', include(router.urls)),
    path('password-change/<int:pk>/', UserProfileUpdateView.as_view(), name='password-change'),
    path('list/', UserListAPIView.as_view(), name='list'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/<str:encoded_username>/', PasswordResetView.as_view(), name='password-reset'),
    path('user-profile/', UserRetrieveAPIView.as_view(), name='user-profile'),
] + router.urls
