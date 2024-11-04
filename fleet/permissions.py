
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'management':
            return True
        return False


class IsHiring(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'hiring':
            return True
        return False


class IsFleet(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower()  == 'fleet':
            return True
        return False


class IsMaintenance(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'maintenance':
            return True
        return False


class IsSafety(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'safety':
            return True
        return False


class ExcludeDispatchOrELD(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() not in ['dispatch', 'eld']:
            return True
        return False


class IsDispatch(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'dispatch':
            return True
        return False


class IsAccounting(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'accounting':
            return True
        return False


class IsDispatchManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'dispatch manager':
            return True
        return False


class IsUpdater(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'updater':
            return True
        return False


class IsBilling(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'billing':
            return True
        return False


class IsPayroll(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.department.name.lower() == 'payroll':
            return True
        return False
