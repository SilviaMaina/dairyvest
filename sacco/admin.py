from django.contrib import admin
from .models import Sacco, Contribution, Loan, Animal, MilkProduction

admin.site.register(Sacco)
admin.site.register(Contribution)
admin.site.register(Loan)
admin.site.register(Animal)
admin.site.register(MilkProduction)
