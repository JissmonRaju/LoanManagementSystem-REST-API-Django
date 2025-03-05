from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'user', 'amt', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'loan_id')
