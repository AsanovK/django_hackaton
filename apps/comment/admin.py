from django.contrib import admin

from apps.comment.models import Comment

class CommentAdmin(admin.ModelAdmin):
    model = Comment


admin.site.register(Comment, CommentAdmin)