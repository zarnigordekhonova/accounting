from django.db import models
from fleet.models import CustomUser, Driver

# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=100)
    ph_number = models.CharField(max_length=100)
    email = models.EmailField()
    note = models.TextField(null=True, blank=True)
    working_hours = models.TextField(null=True, blank=True)
    need_appointment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'facilities'
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'


class FacilityHistory(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.facility.name

    class Meta:
        db_table = 'facility_history'
        verbose_name = 'Facility History'
        verbose_name_plural = 'Facility Histories'


class Broker(models.Model):
    name = models.CharField(max_length=100)
    mc = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    rep_name = models.CharField(max_length=100)
    rep_ph_number = models.CharField(max_length=100)
    rep_email = models.EmailField()
    billing_email = models.EmailField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brokers'
        verbose_name = 'Broker'
        verbose_name_plural = 'Brokers'


class BrokerHistory(models.Model):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.broker.name

    class Meta:
        db_table = 'broker_history'
        verbose_name = 'Broker History'
        verbose_name_plural = 'Broker Histories'


class LoadProcess(models.Model):
    name = models.CharField(max_length=100)
    order_number = models.IntegerField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'load_processes'
        verbose_name = 'Load Process'
        verbose_name_plural = 'Load Processes'


class Status(models.Model):
    name = models.CharField(max_length=100)
    process = models.ForeignKey(LoadProcess, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'process_statuses'
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Load(models.Model):
    carrier = models.CharField(max_length=100)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='booked_by')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_by')
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    from_facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='from_facility')
    to_facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='to_facility')
    shipment = models.CharField(max_length=100)
    load_number = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    driver_pay = models.DecimalField(max_digits=20, decimal_places=2)
    carrier_pay = models.DecimalField(max_digits=20, decimal_places=2)
    smf_pay = models.DecimalField(max_digits=20, decimal_places=2)
    pickup_date = models.DateField()
    drop_date = models.DateField()
    process = models.ForeignKey(LoadProcess, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.carrier

    class Meta:
        db_table = 'loads'
        verbose_name = 'Load'
        verbose_name_plural = 'Loads'


class LoadHistory(models.Model):
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.load.carrier

    class Meta:
        db_table = 'load_history'
        verbose_name = 'Load History'
        verbose_name_plural = 'Load Histories'


class LoadFile(models.Model):
    name = models.CharField(max_length=100)
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    file = models.FileField(upload_to='loads/')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.load.carrier

    class Meta:
        db_table = 'load_files'
        verbose_name = 'Load File'
        verbose_name_plural = 'Load Files'