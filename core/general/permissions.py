from django.shortcuts import redirect
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAdminUser  # noqa: F401


class IsForeforeAdminUser(BasePermission):

    def has_permission(self, request, view):
        if view.__module__.startswith(('core.products.')):

            if not request.user or request.user.is_authenticated:
                if request.accepted_renderer.format == 'html':
                    raise PermissionDenied(detail=redirect('/manager/login'))
                else:
                    return False

            return request.user.is_staff

            # return IsAdminUser().has_permission(request, view)
        return True
