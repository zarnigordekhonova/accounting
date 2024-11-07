from django.shortcuts import render
from .serializers import DriverDispatcherViewSerializer, DriverDispatcherWriteSerializer
from .models import DriverDispatcher
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from fleet.models import Driver, CustomUser
from fleet.permissions import IsAdminUser, IsDispatchManager, IsUpdater, IsDispatch
from fleet.serializers import DriverViewSerializer, UserListSerializer


class DispatcherListViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsDispatchManager | IsAdminUser | IsUpdater]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return DriverDispatcherWriteSerializer
        return DriverDispatcherViewSerializer

    def get_queryset(self):
        user = self.request.user
        user_company = user.company
        user_department = user.department.name.lower()
        if user_department == 'dispatch':
            return DriverDispatcher.objects.filter(dispatch=user)
        elif user_department == 'management':
            return DriverDispatcher.objects.all()
        elif user_department in ['dispatch manager', 'updater']:
            return DriverDispatcher.objects.filter(dispatch__company=user_company)
        return DriverDispatcher.objects.none()


class DriverByCompanyView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DriverViewSerializer

    def get_queryset(self):
        company = self.request.user.company
        active_drivers = Driver.objects.filter(status__name__iexact='active')
        if self.request.user.department.name.lower() == 'management':
            return Driver.objects.all()
        else:
            return active_drivers.filter(company=company)


class UsersByCompanyView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer

    def get_queryset(self):
        company = self.request.user.company
        if self.request.user.department.name.lower() == 'management':
            return CustomUser.objects.all()
        elif self.request.user.department.name.lower() in ['dispatch manager', 'updater']:
            return CustomUser.objects.filter(company=company)
        else:
            return None
