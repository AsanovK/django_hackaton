import re
from rest_framework import serializers

from config.settings import TWILIO_NUMBER
from .utils import normalize_phone
from .tasks import send_activation_sms
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser, UserManager

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('nickname', 'phone', 'password', 'password_confirm')

    def validate_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('This nickname is already taken. Please choose another one')
        return nickname

    def validate_phone(self, phone):
        phone = normalize_phone(phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Invalid phone format')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Phone already exists')
        return phone

    def validate(self, attrs: dict):
        print(attrs)
        password1 = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if not any(i for i in password1 if i .isdigit()):
            raise serializers.ValidationError('Password must contain at least one digit')
        if password1 != password_confirm:
            raise serializers.ValidationError('Passwort do not match')
        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_sms.delay(user.phone, user.activation_code)
        return user

class LoginSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_nickname(self, nickname):
        if not User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("User not found!")
        return nickname

    def validate(self, data):
        request = self.context.get('request')
        nickname = data.get('nickname')
        password = data.get('password')
        if nickname and password:
            user = authenticate(
                nickname=nickname,
                password = password,
                request = request
            )
            if not user:
                raise serializers.ValidationError("wrong credentials")
        else:
            raise serializers.ValidationError("Nickname and password are required!")
        data['user'] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, required=True)
    new_password = serializers.CharField(min_length=6, required=True)
    new_password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Enter valid password!")
        return old_password

    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError("Password didn't match!")
        return attrs

    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()
        

class ForgotPasswordSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=True)

    def validate_email(self, nickname):
        if not User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError('User not found!')
        return nickname

    def send_verification_sms(self):
        print(self.validated_data)
        nickname = self.validated_data.get('nickname')
        # print(phone)
        user = User.objects.get(nickname=nickname)
        print(user)
        user.create_activation_code()
        send_activation_sms(user.phone, user.activation_code)


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirmation')
        if not User.objects.filter(phone=phone, activation_code=code).exists():
            raise serializers.ValidationError('User not found!')
        if password1 != password2:
            raise serializers.ValidationError("Password didn't match")
        return attrs

    def set_new_password(self):
        phone = self.validated_data.get('phone')
        password = self.validated_data.get('password')
        user = User.objects.get(phone=phone)
        user.set_password(password)
        user.save()