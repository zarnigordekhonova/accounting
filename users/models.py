from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Branches(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Branches"
        db_table = 'branches'
        verbose_name = "Branch"


class Roles(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Roles"
        db_table = 'roles'
        verbose_name = "Role"


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "CustomUsers"
        verbose_name = "CustomUser"
        db_table = "users"
        ordering = ['id']


class UserRoles(models.Model):
    roles = models.ManyToManyField(Roles)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "User Roles"
        db_table = 'user_roles'

    def __str__(self):
        return f"{self.user.username} - {", ".join([role.name for role in self.roles.all()])}"


class PasswordReset(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name_plural = "Reset Passwords"
        verbose_name = "Reset Password"
        db_table = "reset_passwords"
        ordering = ['-created_at']
