from django.urls import path

from apps.account.serializers import ChangePasswordSerializer
from .views import ChangePasswordView, ForgotPasswordCompleteView, ForgotPasswordView, RegistrationView, ActivationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:code>/', ActivationView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_confirm/', ForgotPasswordCompleteView.as_view()),
]