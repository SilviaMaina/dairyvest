#!/usr/bin/python3
"""Django REST Framework serializers for Sacco models"""

from rest_framework import serializers
from .models import Sacco, Contribution, Loan, Animal, MilkProduction


class SaccoSerializer(serializers.ModelSerializer):
    """Serializer for SACCO model"""
    class Meta:
        model = Sacco
        fields = '__all__'


class ContributionSerializer(serializers.ModelSerializer):
    """Serializer for Contribution model"""
    class Meta:
        model = Contribution
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model"""
    class Meta:
        model = Loan
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    """Serializer for Animal model"""
    class Meta:
        model = Animal
        fields = '__all__'


class MilkProductionSerializer(serializers.ModelSerializer):
    """Serializer for MilkProduction model"""
    class Meta:
        model = MilkProduction
        fields = '__all__'
