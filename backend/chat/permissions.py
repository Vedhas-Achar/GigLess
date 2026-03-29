from rest_framework.permissions import BasePermission


class IsConversationParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id in [obj.user_one_id, obj.user_two_id]
