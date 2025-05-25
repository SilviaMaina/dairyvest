from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# Register all your viewsets here
router.register(r'contributions', views.ContributionViewSet, basename='contribution')
router.register(r'loans', views.LoanViewSet, basename='loan')
router.register(r'animals', views.AnimalViewSet, basename='animal')
router.register(r'milk-production', views.MilkProductionViewSet, basename='milkproduction')
router.register(r'saccos', views.SaccoViewSet, basename='sacco')  # Make sure this one exists

urlpatterns = [
    path('', include(router.urls)),
]
