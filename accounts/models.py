from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings


class Role(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    FINANCE_MANAGER = 'FINANCE_MANAGER', 'Finance Manager'
    USER = 'USER', 'User'

class Sacco(models.Model):
        sacco = models.CharField(max_length=150, unique=True)
        
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.sacconame
          



class CustomUserManager(BaseUserManager):
    def create_user(self,email,username,password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.SUPER_ADMIN)
        if extra_fields.get('is_staff') is not True:
           raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
           raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != Role.SUPER_ADMIN:
           raise ValueError('Superuser must have role of Super Admin.')
        
        extra_fields.setdefault('firstname', username)
        extra_fields.setdefault('lastname', 'Admin') 

        extra_fields.pop('sacconame', None)
        extra_fields.pop('phone_number', None)

        return self.create_user(email,username,password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150,blank=True)
    lastname = models.CharField(max_length=150,blank=True)
    role = role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = CloudinaryField('image', blank=True, null=True, default='https://res.cloudinary.com/demo/image/upload/sample.jpg')
    sacconame = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='members')
    date_joined = models.DateTimeField(default=timezone.now)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)





    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','firstname','lastname']

    objects = CustomUserManager()



    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.firstname} {self.lastname} ".strip()
    
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
    



    
