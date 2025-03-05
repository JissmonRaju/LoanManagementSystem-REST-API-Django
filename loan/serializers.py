from rest_framework import serializers
from loan.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_id', 'user', 'status', 'amt', 'tenure', 'interest', 'total_to_pay', 'monthly_pay']
        read_only_fields = ['loan_id', 'total_to_pay', 'monthly_pay', 'user']


