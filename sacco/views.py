#!/usr/bin/python3
"""Django REST Framework views for Sacco app"""

from rest_framework import viewsets, permissions
from .models import Sacco, Contribution, Loan, Animal, MilkProduction
from .serializers import (
    SaccoSerializer,
    ContributionSerializer,
    LoanSerializer,
    AnimalSerializer,
    MilkProductionSerializer
)


class SaccoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SACCO instances.
    Supports full CRUD functionality.
    """
    queryset = Sacco.objects.all()
    serializer_class = SaccoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contributions.
    Only accessible to authenticated users.
    """
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing loan records.
    Only accessible to authenticated users.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnimalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing animals owned by members.
    Only accessible to authenticated users.
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]


class MilkProductionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing milk production entries.
    Only accessible to authenticated users.
    """
    queryset = MilkProduction.objects.all()
    serializer_class = MilkProductionSerializer
    permission_classes = [permissions.IsAuthenticated]