from django.urls import path
from .views import CreateCommentView, RetrieveEditDestroyCommentView


urlpatterns = [
    path('', CreateCommentView.as_view()),
    path('<int:pk>', RetrieveEditDestroyCommentView.as_view()),
]