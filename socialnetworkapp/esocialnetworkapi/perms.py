from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.creator == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerOrPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or obj.post.user == request.user
