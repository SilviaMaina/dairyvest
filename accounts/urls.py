from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
  
    MyTokenObtainPairView,
    custom_login_view,
    SuperAdminRegistrationView,
    FinanceManagerRegistrationView,
    UserRegistrationView,
    UserViewSet
)



router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='user')

urlpatterns = [
   
    # JWT token login
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Optional custom login endpoint
    path('login/', custom_login_view, name='custom_login'),

    # Role-based registration
    path('register/superadmin/', SuperAdminRegistrationView.as_view(), name='register_superadmin'),
    path('register/financemanager/', FinanceManagerRegistrationView.as_view(), name='register_financemanager'),
    path('register/user/', UserRegistrationView.as_view(), name='register_user'),

    # UserViewSet (CRUD)
    path('', include(router.urls)),
]
