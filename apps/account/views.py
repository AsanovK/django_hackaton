from rest_framework.views import APIView
from .serializers import ForgotPasswordCompleteSerializer, ForgotPasswordSerializer, LoginSerializer, RegistrationSerializer, ChangePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

User = get_user_model()

class RegistrationView(APIView):
    def post(self, request):
        print(request)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Thanks for registration! Please activate your account', status=201)
        return Response(serializer.errors, status=400)

class ActivationView(APIView):
    def get(self, request, code):
        user = User.objects.filter(activation_code=code).first()
        if user:
            user.is_active = True
            user.save()
            return Response(
                'Your account is activated',
                status=200
            )
        return Response('Invalid activation code', status=400)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Success!')
            
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_sms()
            return Response("Sms sent for recoverying your password")

class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response("Password Changed Successfully")