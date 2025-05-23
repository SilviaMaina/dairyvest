from rest_framework import permissions
from .models import Role 

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Role.SUPER_ADMIN

class IsFinanceManager(permissions.BasePermission): 
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Role.FINANCE_MANAGER

class IsUser(permissions.BasePermission): 
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Role.USER

class IsOwnerOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
       
        if isinstance(obj, request.user.__class__): 
            return obj == request.user or request.user.role == Role.SUPER_ADMIN
        
        
        has_owner_attr = hasattr(obj, 'user') or hasattr(obj, 'owner')
        if has_owner_attr:
            obj_owner = getattr(obj, 'user', getattr(obj, 'owner', None))
            return obj_owner == request.user or request.user.role == Role.SUPER_ADMIN
        
        return False 