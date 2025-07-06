from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import base64

# class SignupView(APIView):
#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             # 🔒 Encrypt the ID
#             encoded_id = base64.urlsafe_b64encode(str(user.id).encode()).decode()
            
#             verify_link = f"http://localhost:8000/api/verify/{encoded_id}/"

#             # Send Email (Console email for now)
#             send_mail(
#                 'Verify your email',
#                 f'Click the link to verify: {verify_link}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 fail_silently=False,
#             )
            
#             return Response({"message": "User created. Please check your email to verify."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from .serializers import SignupSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 🔐 Encode user ID
            encoded_id = base64.urlsafe_b64encode(str(user.id).encode()).decode()
            verify_link = f"http://localhost:8000/api/verify/{encoded_id}/"

            # ✉️ Send email
            send_mail(
                'Verify your email',
                f'Click the link to verify your account:\n\n{verify_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            # ✅ Return token link for Postman automation (DEV ONLY)
            return Response({
                "message": "User created. Please check your email to verify.",
                "verification_token": encoded_id,  # 👈 for Postman auto test
                "verify_link": verify_link         # optional, for display
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import CustomUser

class VerifyEmailView(APIView):
    def get(self, request, encoded_id):
        try:
            # Step 1: Decode Base64 user ID
            user_id = base64.urlsafe_b64decode(encoded_id.encode()).decode()
            
            # Step 2: Find the user
            user = CustomUser.objects.get(id=user_id)

            # Step 3: Mark user as verified & active
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({"message": "✅ Email verified successfully."})
            else:
                return Response({"message": "⚠️ Email is already verified."})

        except CustomUser.DoesNotExist:
            return Response({"error": "❌ User not found."}, status=404)
        except Exception as e:
            return Response({"error": "❌ Invalid or expired verification link."}, status=400)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = serializer.validated_data

        return Response({
            "message": "Login successful",
            "access": tokens.get("access"),
            "refresh": tokens.get("refresh"),
        }, status=status.HTTP_200_OK)
