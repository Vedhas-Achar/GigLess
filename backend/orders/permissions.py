from rest_framework.permissions import BasePermission


class IsOrderParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id in [obj.customer_id, obj.service.freelancer_id]
