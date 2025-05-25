from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class Role(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    FINANCE_MANAGER = 'FINANCE_MANAGER', 'Finance Manager'
    USER = 'USER', 'User'


class Sacco(models.Model):
    sacco = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sacco  # 🔁 Fixed: should return .sacco not .sacconame


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user. Requires sacconame unless user is a superuser.
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        is_superuser = extra_fields.get('is_superuser', False)

        # Enforce sacco requirement only for non-superusers
        if not is_superuser and not extra_fields.get('sacconame'):
            raise ValueError("Regular users must belong to a Sacco.")

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser. Sacconame and phone_number are removed.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.SUPER_ADMIN)
        extra_fields.setdefault('firstname', username)
        extra_fields.setdefault('lastname', 'Admin')

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != Role.SUPER_ADMIN:
            raise ValueError('Superuser must have role of Super Admin.')

        # Remove fields irrelevant for superuser
        extra_fields.pop('sacconame', None)
        extra_fields.pop('phone_number', None)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = CloudinaryField('image', blank=True, null=True, default='https://res.cloudinary.com/demo/image/upload/sample.jpg')

    # 🔧 Allow null=True and blank=True for superusers
    sacconame = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='members', null=True, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}".strip()

    def get_short_name(self):
        return self.firstname

    @property
    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN

    @property
    def is_finance_manager(self):
        return self.role == Role.FINANCE_MANAGER

    @property
    def is_user(self):
        return self.role == Role.USER