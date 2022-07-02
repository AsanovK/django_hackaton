from rest_framework.permissions import BasePermission


class IsCommentAuthor(BasePermission):
    def has_object_permissions(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user