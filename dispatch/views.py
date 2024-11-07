from django.shortcuts import render
from .serializers import DriverDispatcherViewSerializer, DriverDispatcherWriteSerializer
from .models import DriverDispatcher
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from fleet.models import Driver, CustomUser, Department
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
        if user.department.name.lower() == 'dispatch':
            return DriverDispatcher.objects.filter(dispatch=user)
        elif user.department.name.lower() == 'management':
            return DriverDispatcher.objects.all()
        elif user.department.name.lower() in ['dispatch manager', 'updater']:
            return DriverDispatcher.objects.filter(dispatch__company=user.company)
        return None


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
        is_active_dispatch = CustomUser.objects.filter(deparment__name__exact='dispatch',
                                                       is_active=True)
        if self.request.user.department.name.lower() == 'management':
            return CustomUser.objects.all()
        elif self.request.user.department.name.lower() in ['dispatch manager', 'updater']:
            return is_active_dispatch.filter(company=self.request.user.company)
        else:
            return None



