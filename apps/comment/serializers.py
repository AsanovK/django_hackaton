from importlib.resources import read_binary
from xml.etree.ElementTree import Comment
from rest_framework import serializers

from apps.account.serializers import User
from .models import Comment, Product
from rest_framework.permissions import IsAuthenticated

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    # def validate(self, user):
    #     if IsAuthenticated==False:
    #         raise serializers.ValidationError("You must be registered")
    #     else:
    #         return user