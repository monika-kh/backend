from rest_framework import permissions


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return "Employee" in [x.name for x in request.user.groups.all()]


class IsHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return "HR" in [x.name for x in request.user.groups.all()]


class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return "Owner" in [x.name for x in request.user.groups.all()]
