from django.contrib import admin
from django.urls import path, include
from loan.views import loan_list, LoanListCreateView, LoanDetailView, LoanAdminView, LoanStatusUpdateView, \
    loan_foreclose, get_csrf_token
from django.http import HttpResponse


def home(request):
    return HttpResponse("Loan Management System is running!")


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/loans/', loan_list),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('authentication.urls')),
    path('loans/', LoanListCreateView.as_view(), name='loan-list-create'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail'),
    path('admin/loans/', LoanAdminView.as_view(), name='admin-loan-list'),
    path('api/admin/loans/<int:loan_id>/status/', LoanStatusUpdateView.as_view(), name='loan-status-update'),
    path('loans/<int:pk>/foreclose/', loan_foreclose, name='loan-foreclose'),
    path('csrf-token/', get_csrf_token, name='csrf-token')
]
