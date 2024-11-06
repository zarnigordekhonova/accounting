from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, When, IntegerField, F, Window
from django.db.models.functions import RowNumber
from .models import (UserStatus, CustomUser, Department, Company, Recruiter, DriverStatus, Driver, DriverType,
                     Make, Models, TruckStatus, VehicleType, LessorCompany, CarrierType, Truck, TruckDriver)
from .serializers import (UserStatusSerializer, CompanyWriteSerializer, CompanyReadSerializer, DepartmentSerializer,
                          UserProfileUpdateSerializer, UserUpdateSerializer, UserListSerializer, DriverStatusSerializer,
                          RecruiterSerializer, DriverTypeSerializer, DriverViewSerializer, DriverWriteSerializer,
                          ActiveDrivers, MakesSerializer, TruckStatusSerializer, LessorCompanyViewSerializer,
                          TruckDriversWriteSerializer, VehicleTypeViewSerializer, CarrierTypeViewSerializer,
                          TrucksViewSerializer, TrucksWriteSerializer, TruckDriversViewSerializer,
                          TruckDriverSerializer, CustomTokenObtainPairSerializer)
from .permissions import IsHiring, IsFleet, IsAdminUser, IsSafety, IsMaintenance

User = get_user_model()

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CompanyWriteSerializer
        return CompanyReadSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.department.name.lower() == 'management':
            return Department.objects.all()
        else:
            return Department.objects.filter(name=user.department.name)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserStatusViewSet(viewsets.ModelViewSet):
    serializer_class = UserStatusSerializer
    queryset = UserStatus.objects.all()
    permission_classes = [IsAuthenticated]


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]


class UserRetrieveAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.filter(id=user.id)
        return queryset


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]


class DriverStatusViewSet(viewsets.ModelViewSet):
    queryset = DriverStatus.objects.all()
    serializer_class = DriverStatusSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsHiring | IsAdminUser]
        return [permission() for permission in permission_classes]


class RecruiterViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsHiring | IsAdminUser]
        return [permission() for permission in permission_classes]


class DriverTypeViewSet(viewsets.ModelViewSet):
    queryset = DriverType.objects.all()
    serializer_class = DriverTypeSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsHiring | IsAdminUser]
        return [permission() for permission in permission_classes]


class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['full_name', 'driver_id']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(status__name__icontains='Inactive')
        queryset = queryset.annotate(
            active_order=Case(
                When(status__name='Active', then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by('active_order')
        return queryset

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return DriverWriteSerializer
        return DriverViewSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsHiring | IsAdminUser]
        return [permission() for permission in permission_classes]


class DriverRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    permission_classes = [IsAuthenticated, IsHiring | IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return DriverWriteSerializer
        return DriverViewSerializer


class ActiveDriversView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = ActiveDrivers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get('active')
        inactive = self.request.query_params.get('inactive')

        if not active and not inactive:
            queryset = queryset.exclude(status__name='Inactive')

        return queryset


class InActiveDriversView(generics.ListAPIView):
    queryset = Driver.objects.filter(status__name__icontains='Inactive')
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    serializer_class = DriverViewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['full_name', 'driver_id']


class MakesViewSet(viewsets.ModelViewSet):
    queryset = Make.objects.all()
    serializer_class = MakesSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsFleet | IsAdminUser | IsSafety | IsHiring]
        return [permission() for permission in permission_classes]


class TruckStatusesViewSet(viewsets.ModelViewSet):
    queryset = TruckStatus.objects.all()
    serializer_class = TruckStatusSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsFleet | IsAdminUser | IsSafety]
        return [permission() for permission in permission_classes]


class ModelsViewSet(viewsets.ModelViewSet):
    filter_backends = [OrderingFilter]

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsFleet | IsAdminUser | IsSafety]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Models.objects.all()
        make_id = self.request.query_params.get('make')
        if make_id is not None:
            queryset = queryset.filter(make_id=make_id)
            return queryset
        else:
            return None



class TrucksListCreateView(generics.ListCreateAPIView):
    queryset = Truck.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['unit_number', 'VIN', 'carrier_company__name', 'truck_drivers__driver__full_name', 'sub_unit_for__unit_number', 'given_sub__unit_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.department.name.lower() == 'dispatch':
            company = self.request.user.company
            queryset = queryset.filter(carrier_company=company)

        queryset = queryset.annotate(
            enroute_order=Case(
                When(status__name='Enroute', then=0),
                default=1,
                output_field=IntegerField(),
            ),
            row_number=Window(
            expression=RowNumber(),
            partition_by=[F('id')],
            order_by=F('enroute_order').asc()
            )
        )
        queryset = queryset.filter(row_number=1).order_by('enroute_order', 'status__name', 'id')

        return queryset

    def list(self, request, *args, **kwargs):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        filtered_count = filtered_queryset.count()
        active_trucks_count = Truck.objects.exclude(
            status__name__icontains='Inactive'
        ).count()
        response = super().list(request, *args, **kwargs)
        response.data['filtered_count'] = filtered_count
        response.data['active_trucks_count'] = active_trucks_count
        return response

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsFleet | IsAdminUser | IsSafety]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return TrucksWriteSerializer
        return TrucksViewSerializer


class TrucksRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Truck.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsFleet | IsAdminUser | IsSafety | IsHiring | IsMaintenance]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return TrucksWriteSerializer
        return TrucksViewSerializer


class ActiveTrucksListView(generics.ListAPIView):
    serializer_class = TruckDriverSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Truck.objects.exclude(status__name__in=['Inactive', 'Inactive Waiting Docs'])
        return queryset


class TruckDriversListCreateView(generics.ListCreateAPIView):
    queryset = TruckDriver.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsFleet | IsAdminUser | IsSafety | IsHiring | IsMaintenance]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TruckDriversViewSerializer
        return TruckDriversWriteSerializer

    def create(self, request, *args, **kwargs):
        truck_id = request.data.get('truck_id')
        driver_id = request.data.get('driver_id')

        if not truck_id or not driver_id:
            raise ValidationError({"detail": "Truck ID and driver ID are required."})

        try:
            truck = Truck.objects.get(id=truck_id)
            driver = Driver.objects.get(id=driver_id)
        except Truck.DoesNotExist:
            raise ValidationError({"detail": f"Truck with ID {truck_id} does not exist."})
        except Driver.DoesNotExist:
            raise ValidationError({"detail": f"Driver with ID {driver_id} does not exist."})

        if TruckDriver.objects.filter(truck=truck, driver=driver).exists():
            return Response({
                "message": "Driver already assigned to this truck.",
                "truck_id": truck_id,
                "driver_id": driver_id
            }, status=200)

        TruckDriver.objects.create(truck=truck, driver=driver)

        return Response({
            "message": "Truck driver created successfully.",
            "truck_id": truck_id,
            "driver_id": driver_id
        }, status=201)


class TruckDriversRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TruckDriver.objects.all()
    serializer_class = TruckDriversWriteSerializer
    permission_classes = [IsFleet | IsAdminUser | IsSafety | IsHiring | IsMaintenance]


class LessorCompanyView(generics.ListAPIView):
    queryset = LessorCompany.objects.all()
    serializer_class = LessorCompanyViewSerializer
    permission_classes = [IsAuthenticated]


class VehicleTypeView(generics.ListAPIView):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeViewSerializer
    permission_classes = [IsAuthenticated]


class CarrierTypeView(generics.ListAPIView):
    queryset = CarrierType.objects.all()
    serializer_class = CarrierTypeViewSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


