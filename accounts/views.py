from django.contrib.auth import authenticate
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Role
from .serializers import (
    RegisterUserSerializer, 
    UserDetailSerializer, 
    MyTokenObtainPairSerializer, 
    LoginRequestSerializer
)
from .permissions import IsSuperAdmin, IsOwnerOrAdmin


# JWT Token View
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Abstract base registration view to avoid duplication
class UserRegistrationBaseView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer

    def perform_create(self, serializer):
        serializer.save(
            role=getattr(self, 'role_to_set', Role.USER),
            is_staff=getattr(self, 'is_staff_status', False),
            is_superuser=getattr(self, 'is_superuser_status', False),
        )


# Super Admin registration endpoint
class SuperAdminRegistrationView(UserRegistrationBaseView):
    permission_classes = [AllowAny]  # Or use [IsSuperAdmin] for tighter control
    role_to_set = Role.SUPER_ADMIN
    is_staff_status = True
    is_superuser_status = True


# Finance Manager registration endpoint (only accessible by Super Admins)
class FinanceManagerRegistrationView(UserRegistrationBaseView):
    permission_classes = [IsSuperAdmin]
    role_to_set = Role.FINANCE_MANAGER
    is_staff_status = True


# Regular User registration endpoint
class UserRegistrationView(UserRegistrationBaseView):
    permission_classes = [AllowAny]
    role_to_set = Role.USER


# Custom login endpoint (instead of default JWT view)
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login_view(request):
    serializer = LoginRequestSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request=request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = MyTokenObtainPairSerializer.get_token(user)
            return Response({
                'message': 'Login successful',
                'user': UserDetailSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials or inactive account.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User management viewset with RBAC controls
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsSuperAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        elif self.action == 'destroy':
            permission_classes = [IsSuperAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)