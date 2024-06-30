from rest_framework import permissions


class IsSubscribed(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_subscribed
