from rest_framework.permissions import BasePermission
from users.models import RoleChoices
class IsInstructor(BasePermission) :

    def has_permission(self, request, view):
        return request.user.role == RoleChoices.INSTRUCTOR
    