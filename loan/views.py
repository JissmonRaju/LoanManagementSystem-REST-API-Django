from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from loan.models import Loan
from loan.serializers import LoanSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.middleware.csrf import get_token
import calendar
from math import pow
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status


@api_view(['GET', 'POST'])
def loan_list(request):
    if request.method == 'GET':
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoanListCreateView(generics.ListCreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)


class LoanAdminView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]
    queryset = Loan.objects.all()


class LoanStatusUpdateView(generics.UpdateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]
    queryset = Loan.objects.all()
    lookup_field = 'loan_id'

    def patch(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Proper check for admin status
            return JsonResponse({'error': 'Please login as an admin to update status.'}, status=403)

        loan = self.get_object()
        status = request.data.get('status')

        if status in ['approved', 'rejected', 'closed']:
            loan.status = status
            loan.save()
            return JsonResponse({'status': f'Loan status updated to {status}.'})

        return JsonResponse({'error': 'Invalid status.'}, status=400)


@api_view(['POST'])
def loan_foreclose(request, pk):
    try:
        loan = Loan.objects.get(pk=pk, user=request.user)
        if loan.status != 'approved':
            return Response({'error': 'Loan must be approved to foreclose.'}, status=400)

        loan.status = 'closed'
        loan.save()
        return Response({'message': 'Loan foreclosed successfully.'})
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found.'}, status=404)


@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def add_months(source_date, months):
    """
    Adds a given number of months to source_date.
    Handles month/year roll-over.
    """
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day).date()


def generate_payment_schedule(loan):
    """
    Generate a payment schedule for a loan.
    EMI Formula:
      EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    where:
      P = principal (loan.amount)
      r = monthly interest rate (loan.interest_rate / 100 / 12)
      n = number of months (loan.tenure)
    """
    schedule = []
    principal = loan.amt
    n = loan.tenure  # total number of months
    # Monthly interest rate as a decimal
    r = (loan.interest / 100) / 12


    if r != 0:
        emi = principal * r * pow(1 + r, n) / (pow(1 + r, n) - 1)
    else:
        emi = principal / n

    # Use loan.created_at as the start date if available; otherwise, use today.
    start_date = loan.created_at.date() if loan.created_at else datetime.now().date()

    for i in range(1, n + 1):
        due_date = add_months(start_date, i)
        schedule.append({
            "installment_no": i,
            "due_date": due_date.isoformat(),
            "amt": round(emi, 2)
        })
    return schedule


class PaymentScheduleView(APIView):
    """
    GET /api/loans/<pk>/schedule/
    Returns the generated payment schedule for the specified loan.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            # Ensure the loan belongs to the current user (or adjust as per your access rules)
            loan = Loan.objects.get(pk=pk, user=request.user)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)

        schedule = generate_payment_schedule(loan)
        return Response({
            "status": "success",
            "loan_id": loan.pk,
            "payment_schedule": schedule
        }, status=status.HTTP_200_OK)
