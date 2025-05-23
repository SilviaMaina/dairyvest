from django.db import models
from django.utils import timezone
from django.conf import settings
from accounts.models import Sacco,Role




class Contribution(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions', limit_choices_to={'role': Role.USER})
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='sacco_contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_date = models.DateField(auto_now_add=True)
    contribution_type = models.CharField(max_length=50, default='monthly')     
    

    def __str__(self):
        return f"{self.member.username} - {self.amount} - {self.contribution_date}"

class Loan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REPAID', 'Repaid'),
        ('DEFAULTED', 'Defaulted'),
    ]
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans', limit_choices_to={'role': Role.USER})
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='sacco_loans')
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Loan for {self.member.username} - {self.amount_requested} ({self.status})"
class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Repayment for loan {self.loan.id} - {self.amount_paid}"
    
class Animal(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='animals', limit_choices_to={'role': Role.USER})
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='sacco_animals')
    animal_type = models.CharField(max_length=50, default='Cow')
    tag_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    count = models.PositiveIntegerField(default=1)
    date_acquired = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.animal_type} ({self.tag_number or 'Group'}) - Owner: {self.owner.username}"

class MilkProduction(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='milk_records', limit_choices_to={'role': Role.USER})
    sacco = models.ForeignKey(Sacco, on_delete=models.CASCADE, related_name='sacco_milk_production')
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True, related_name='milk_production')
    litres_produced = models.DecimalField(max_digits=7, decimal_places=2)
    date_recorded = models.DateField()
    time_recorded = models.TimeField(null=True, blank=True)
    price_per_litre = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.farmer.username} - {self.litres_produced}L on {self.date_recorded}"


