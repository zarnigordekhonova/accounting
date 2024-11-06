from rest_framework import generics, filters, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from fleet.views import CustomPagination
from .models import (Facility, FacilityHistory, Broker, BrokerHistory, LoadProcess,
                     Status, Load, LoadHistory, LoadFile, LoadStop)
from .serializers import (BrokersSerializer, BrokerHistoryViewSerializer,
                          BrokerHistoryWriteSerializer, FacilitySerializer, FacilityHistoryViewSerializer, FacilityHistoryWriteSerializer, LoadStopViewSerializer,
                          LoadProcessesSerializer, StatusesViewSerializer, StatusesWriteSerializer, LoadsViewSerializer, LoadUseSerializer, LoadStopWriteSerializer,
                          LoadsWriteSerializer, LoadHistoryViewSerializer, LoadHistoryWriteSerializer, LoadFilesViewSerializer, LoadFilesWriteSerializer)
from fleet.permissions import IsAdminUser, IsBilling, IsDispatch, IsDispatchManager, IsUpdater

class BrokerHistoryViewSet(viewsets.ModelViewSet):
    queryset = BrokerHistory.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return BrokerHistoryWriteSerializer
        return BrokerHistoryViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]


class FacilityHistoryViewSet(viewsets.ModelViewSet):
    queryset = FacilityHistory.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return FacilityHistoryWriteSerializer
        return FacilityHistoryViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(changed_by=self.request.user)


class FacilitiesViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        facility = serializer.save()
        FacilityHistory.objects.create(
            facility=facility,
            changed_by=self.request.user,
            description="Facility created",
            created_at=facility.created_at
        )

    def perform_update(self, serializer):
        facility = self.get_object()
        original_data = FacilitySerializer(facility).data
        updated_facility = serializer.save()
        ignore_fields = {'created_at', 'last_updated'}
        changes = []
        for field, old_value in original_data.items():
            if field in ignore_fields:
                continue
            new_value = getattr(updated_facility, field)
            if old_value != new_value:
                changes.append(f"{field.capitalize()}: {old_value} -> {new_value}")
        description = "Facility updated. " + " | ".join(changes) if changes else "No significant changes made."
        FacilityHistory.objects.create(
            facility=facility,
            changed_by=self.request.user,
            description=description
        )


class BrokersViewSet(viewsets.ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokersSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        broker = serializer.save()
        BrokerHistory.objects.create(
            broker=broker,
            changed_by=self.request.user,
            description="Broker created",
            created_at=broker.created_at
        )

    def perform_update(self, serializer):
        broker = self.get_object()
        original_data = BrokersSerializer(broker).data
        updated_broker = serializer.save()
        ignore_fields = {'created_at', 'last_updated'}
        changes = []
        for field, old_value in original_data.items():
            if field in ignore_fields:
                continue
            new_value = getattr(updated_broker, field)
            if old_value != new_value:
                changes.append(f"{field.capitalize()}: {old_value} -> {new_value}")
        description = "Broker updated. " + " | ".join(changes) if changes else "No significant changes made."
        BrokerHistory.objects.create(
            broker=broker,
            changed_by=self.request.user,
            description=description
        )


class LoadsViewSet(viewsets.ModelViewSet):
    queryset = Load.objects.all()

    def get_queryset(self):
        return Load.objects.select_related('process').order_by('process__order_number')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return LoadsWriteSerializer
        return LoadsViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        load = serializer.save()
        LoadHistory.objects.create(
            load=load,
            changed_by=self.request.user,
            description="Load created",
            created_at=load.created_at
        )

    def perform_update(self, serializer):
        load = self.get_object()
        original_data = LoadUseSerializer(load).data
        updated_load = serializer.save()
        ignore_fields = {'created_at', 'last_updated'}
        changes = []
        old_values = {}
        field_mappings = {
            'booked_by': lambda obj: obj.booked_by.username if obj.booked_by else None,
            'created_by': lambda obj: obj.created_by.username if obj.created_by else None,
            'from_facility': lambda obj: obj.from_facility.name if obj.from_facility else None,
            'broker': lambda obj: obj.broker.name if obj.broker else None,
            'driver': lambda obj: obj.driver.full_name if obj.driver else None,
            'process': lambda obj: obj.process.name if obj.process else None,
        }

        for field in original_data:
            if field in field_mappings:
                old_values[field] = field_mappings[field](load)
            else:
                old_values[field] = getattr(load, field)

        for field, old_value in old_values.items():
            if field in ignore_fields:
                continue
            if field in field_mappings:
                new_value = field_mappings[field](updated_load)
            else:
                new_value = getattr(updated_load, field)
            if str(old_value) != str(new_value):
                changes.append(f"{field.replace('_', ' ').title()}: {old_value} -> {new_value}")

        description = "Load updated. " + " | ".join(changes) if changes else "No significant changes made."
        LoadHistory.objects.create(
            load=load,
            changed_by=self.request.user,
            description=description
        )


class LoadProcessesViewSet(viewsets.ModelViewSet):
    queryset = LoadProcess.objects.all()
    serializer_class = LoadProcessesSerializer
    ordering = ['order_number']

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]


class StatusesViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return StatusesWriteSerializer
        return StatusesViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]


class LoadHistoryViewSet(viewsets.ModelViewSet):
    queryset = LoadHistory.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return LoadHistoryWriteSerializer
        return LoadHistoryViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(changed_by=self.request.user)


class LoadFilesViewSet(viewsets.ModelViewSet):
    queryset = LoadFile.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return LoadFilesWriteSerializer
        return LoadFilesViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]


class LoadStopsViewSet(viewsets.ModelViewSet):
    queryset = LoadStop.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return LoadStopWriteSerializer
        return LoadStopViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsDispatch | IsDispatchManager | IsUpdater | IsBilling]
        return [permission() for permission in permission_classes]


class BrokerByIdAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BrokerHistoryViewSerializer

    def get_queryset(self):
        broker = self.kwargs.get('pk')
        return BrokerHistory.objects.filter(broker=broker)


class FacilityByIdAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FacilityHistoryViewSerializer

    def get_queryset(self):
        facility = self.kwargs.get('pk')
        return FacilityHistory.objects.filter(facility=facility)


class LoadByIdAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoadHistoryViewSerializer

    def get_queryset(self):
        load = self.kwargs.get('pk')
        return LoadHistory.objects.filter(load=load)

