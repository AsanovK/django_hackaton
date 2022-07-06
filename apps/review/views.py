from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Review, Like
from .serializers import ReviewSerializer
from .permissions import IsReviewAuthor
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = IsReviewAuthor
    

    def get_permissions(self):
        if self.action in ['list', 'reetryece']:
            permissions = []
        elif self.action == 'like':
            permissions = [IsAuthenticated, ]
        elif self.action == 'favorite':
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsReviewAuthor, ]
        return [permission() for permission in permissions]

    @action(detail=True, methods=['POST'])
    def like(self, request, *args, **kwargs):
        review = self.get_object()
        like_obj, _ = Like.objects.get_or_create(review=review, user=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'like'
        if not like_obj.like:
            status = 'unlike'
        return Response({'status': status})

    @action(detail=True, methods=['POST'])
    def favorite(self, request, *args, **kwargs):
        review = self.get_object()
        favorite_obj, _ = Like.objects.get_or_create(review=review, user=request.user)
        favorite_obj.like = not favorite_obj.like
        favorite_obj.save()
        status = 'favorite'
        if not favorite_obj.like:
            status = 'not in the favorites'
        return Response({'status': status})