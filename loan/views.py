from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from loan.models import Loan
from loan.serializers import LoanSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from django.middleware.csrf import get_token


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
