from django.urls import path

from .views import ProductListView, ProductDetailView, ProductCreateView


urlpatterns = [
    path('', ProductListView.as_view()),
    path('create/', ProductCreateView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
]