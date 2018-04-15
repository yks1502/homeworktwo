from rest_framework import permissions


class IsOwner(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if obj.user1 == request.user or obj.user2 == request.user:
      return True