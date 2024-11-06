from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class UserStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = " User Statuses"
        verbose_name = "Status"
        db_table = "user_statuses"
        ordering = ['id']


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}. {self.name}"

    class Meta:
        verbose_name_plural = "Departments"
        verbose_name = "Department"
        db_table = "departments"
        ordering = ['id']


class Company(models.Model):
    name = models.CharField(max_length=100)
    status = models.ForeignKey(UserStatus, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}. {self.name}"

    class Meta:
        verbose_name_plural = "Companies"
        verbose_name = "Company"
        db_table = "companies"
        ordering = ['id']


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "CustomUsers"
        verbose_name = "CustomUser"
        db_table = "users"
        ordering = ['id']


class Recruiter(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Recruiters"
        db_table = "recruiters"


class DriverType(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = "Driver Types"
        db_table = "driver_types"


class DriverStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = " Driver Statuses"
        db_table = "driver_statuses"


class Driver(models.Model):
    full_name = models.CharField(max_length=80)
    SSN = models.CharField(max_length=100, null=True, blank=True)
    driver_id = models.CharField(max_length=30, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(DriverStatus, on_delete=models.CASCADE, null=True, blank=True)
    driver_type = models.ForeignKey(DriverType, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'drivers'
        verbose_name_plural = "Drivers"


class Make(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}.{self.name}"

    class Meta:
        ordering = ['id']
        db_table = 'makes'
        verbose_name_plural = 'Makes'


class Models(models.Model):
    name = models.CharField(max_length=50)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}.{self.name}"

    class Meta:
        ordering = ['id']
        db_table = 'models'
        verbose_name_plural = 'Models'


class TruckStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}.{self.name}"

    class Meta:
        ordering = ['id']
        db_table = 'truck_statuses'
        verbose_name_plural = 'Truck Statuses'


class LessorCompany(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lessor_companies'
        verbose_name_plural = 'Lessor Companies'


class VehicleType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vehicle_types'
        verbose_name_plural = 'Vehicle Types'


class CarrierType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'carrier_types'
        verbose_name_plural = 'Carrier Types'


class Truck(models.Model):
    unit_number = models.CharField(max_length=40)
    VIN = models.CharField(max_length=17)
    status = models.ForeignKey(TruckStatus, on_delete=models.CASCADE)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    lessor_company = models.ForeignKey(LessorCompany, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)
    owner_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    carrier_type = models.ForeignKey(CarrierType, on_delete=models.CASCADE, null=True, blank=True)
    carrier_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='carrier_company')

    def __str__(self):
        return self.unit_number

    class Meta:
        ordering = ['-id']
        db_table = 'trucks'
        verbose_name_plural = 'Trucks'


class TruckDriver(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='truck_drivers')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.driver.full_name} - {self.truck.unit_number}"

    class Meta:
        ordering = ['-id']
        db_table = 'truck_drivers'
        verbose_name_plural = 'Truck Drivers'

