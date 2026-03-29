from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerFreelancerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.freelancer_id == request.user.id
