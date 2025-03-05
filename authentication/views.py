from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
import random
from rest_framework import status
from .models import UserOTP


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    send_mail(
        'Your Loan Management System OTP',
        f'Your OTP is: {otp}',
        'jissmonraju25@gmail.com',
        [email],
        fail_silently=False,
    )


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        UserOTP.objects.update_or_create(
            user=user,
            defaults={'otp': otp, 'created_at': now(), 'expires_at': now() + timedelta(minutes=5)}
        )
        send_otp_email(user.email, otp)

        return Response({'message': 'OTP sent successfully'})


class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user_otp = UserOTP.objects.filter(user=user).order_by('-created_at').first()
        if not user_otp or user_otp.otp != otp or now() > user_otp.expires_at:
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        user_otp.is_verified = True
        user_otp.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'OTP verified successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            otp = generate_otp()
            UserOTP.objects.update_or_create(
                user=user,
                defaults={'otp': otp, 'created_at': now(), 'expires_at': now() + timedelta(minutes=5)}
            )
            send_otp_email(user.email, otp)
            request.session['email'] = email
            return Response({'message': 'OTP sent to your email. Please verify.'})

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.values('id', 'username', 'email')
        return Response(users)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
