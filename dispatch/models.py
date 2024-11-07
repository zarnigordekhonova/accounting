from django.db import models

# Create your models here.


class DriverDispatcher(models.Model):
    from fleet.models import CustomUser, Driver
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    dispatch = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.dispatch.name

    class Meta:
        verbose_name_plural = "Driver Dispatchers"
        verbose_name = "Driver Dispatcher"
        db_table = "driver_dispatchers"


