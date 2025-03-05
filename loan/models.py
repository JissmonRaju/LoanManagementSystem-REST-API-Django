import math
from django.db import models
from django.contrib.auth.models import User

class Loan(models.Model):
    LOAN_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    loan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    amt = models.FloatField()
    tenure = models.IntegerField()  # in months
    interest = models.FloatField()  # annual interest rate in %
    total_to_pay = models.FloatField(blank=True, null=True)
    monthly_pay = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.tenure > 0 and self.interest >= 0:
            r = self.interest / 100  # interest rate as decimal
            t = self.tenure / 12  # tenure in years
            n = 12  # compounding frequency (monthly)
            A = self.amt * math.pow((1 + r / n), n * t)

            self.total_to_pay = round(A, 2)
            self.monthly_pay = round(A / self.tenure, 2)

        super().save(*args, **kwargs)
