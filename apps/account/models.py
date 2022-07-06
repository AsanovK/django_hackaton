from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create(self, password, phone, **extra_fields):
        if not phone:
            raise ValueError('Users must have phone number')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(password, **extra_fields)

class CustomUser(AbstractBaseUser):
    nickname = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=14, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()
    
    def __str__(self):
        return self.nickname

    def has_module_perms(self, app_label):
        return  self.is_staff
    
    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=10)
        if CustomUser.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()