from django.urls import path
from .views import RegisterView, LoginView, UserListView, LogoutView, RequestOTPView,OTPVerificationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='users'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),

]
