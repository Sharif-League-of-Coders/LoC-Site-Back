from rest_framework.permissions import BasePermission


class PersonComplete(BasePermission):

    def has_permission(self, request, view):
        return request.user.person.is_complete
