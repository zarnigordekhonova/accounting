from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import (UserStatus, Company, Department, CustomUser, Recruiter, DriverType, DriverStatus, Driver, Make, Models,
                     TruckStatus, LessorCompany, VehicleType, CarrierType, Truck, TruckDriver)

User = get_user_model()


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['id', 'name']
        ref_name = 'user-status'


class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class CompanyReadSerializer(serializers.ModelSerializer):
    status = UserStatusSerializer()
    class Meta:
        model = Company
        fields = ('id', 'name', 'status')

    def get_status(self, obj):
        return obj.status.name


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name']


class DriverStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverStatus
        fields = ('id', 'name')
        ref_name = 'driver-status'


class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ('id', 'name')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'company', 'department', 'is_active']
        extra_kwargs = {
            'id': {'read_only': True},
            'company': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'department': {'read_only': True},
            'is_active': {'read_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'company', 'department', 'is_active']
        extra_kwargs = {
            'username': {'read_only': True},
            'password': {'read_only': True}
        }


class UserListSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField(method_name='get_company')
    department = serializers.SerializerMethodField(method_name='get_department')

    def get_company(self, obj):
        return obj.company.name if obj.company else None

    def get_department(self, obj):
        return obj.department.name if obj.department else None

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'company', 'department', 'is_active']



class DriverTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverType
        fields = ('id', 'name')


class CompanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class DriverViewSerializer(serializers.ModelSerializer):
    company = CompanyViewSerializer()
    status = DriverStatusSerializer()
    recruiter = RecruiterSerializer()
    driver_type = DriverTypeSerializer()

    class Meta:
        model = Driver
        fields = '__all__'


class DriverWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class ActiveDrivers(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ('id', 'full_name')


class MakesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id', 'name']


class TruckStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckStatus
        fields = ['id', 'name']


class ModelsViewSerializer(serializers.ModelSerializer):
    make = MakesSerializer()

    class Meta:
        model = Models
        fields = ['id', 'name', 'make']


class ModelsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = '__all__'


class ModelsUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = ['id', 'name']


class LessorCompanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessorCompany
        fields = ['id', 'name']


class VehicleTypeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name']


class CarrierTypeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierType
        fields = ['id', 'name']

class TrucksViewSerializer(serializers.ModelSerializer):
    model = serializers.SerializerMethodField(method_name='get_model')
    status = TruckStatusSerializer()
    make = MakesSerializer()
    lessor_company = LessorCompanyViewSerializer()
    vehicle_type = VehicleTypeViewSerializer()
    carrier_type = CarrierTypeViewSerializer()
    owner_company = CompanyUseSerializer()
    carrier_company = CompanyUseSerializer()

    def get_driver(self, obj):
        drivers = TruckDriver.objects.filter(truck=obj)
        return [{"id": driver.driver.id, "name": driver.driver.full_name, "truck_driver_id": driver.id} for driver in drivers]

    def get_model(self, obj):
        return obj.model.name

    class Meta:
        model = Truck
        fields = '__all__'


class TrucksWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

    def validate_VIN(self, value):
        from .utils import is_valid_vin
        if not is_valid_vin(value):
            raise serializers.ValidationError("Invalid VIN number. The VIN must be exactly 17 characters long and can only contain valid characters.")
        return value


class TruckSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField(method_name='get_driver')
    make = MakesSerializer()
    model = ModelsUseSerializer()

    def get_driver(self, obj):
        drivers = TruckDriver.objects.filter(truck=obj)
        return [{"id": driver.driver.id, "name": driver.driver.full_name} for driver in drivers]

    class Meta:
        model = Truck
        fields = ['id', 'unit_number', 'VIN', 'make', 'model', 'driver']


class TruckDriverSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = ['id', 'unit_number', 'VIN', 'driver']

    def get_driver(self, obj):
        try:
            truck_drivers = obj.truck_driver.all()
            return [
                {
                'id': truck_driver.driver.id,
                'full_name': truck_driver.driver.full_name
            }
            for truck_driver in truck_drivers
            ]
        except (TruckDriver.DoesNotExist, AttributeError):
            return []


class TruckDriversViewSerializer(serializers.ModelSerializer):
    truck = TrucksViewSerializer()
    driver = DriverViewSerializer()

    class Meta:
        model = TruckDriver
        fields = ['id', 'truck', 'driver', 'start_date']


class TruckDriversWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckDriver
        fields = ['id', 'truck', 'driver', 'start_date']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_active:
            raise serializers.ValidationError("User is not active")

        data.update({
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'department': self.user.department.name if self.user.department else None,
            'company': self.user.company.name if self.user.company else None
        })

        return data
