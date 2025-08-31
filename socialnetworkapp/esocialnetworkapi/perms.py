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



class OwnerPerms(permissions.BasePermission):
    def has_permission(self, request, view):
        # Chỉ cho phép nếu user đã đăng nhập
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Chỉ cho phép thay đổi thông tin của chính user
        return obj == request.user
