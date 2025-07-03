from django.shortcuts import render

from .utils import decode_encrypted_token
from .models import CustomUser
from .utils import decode_encrypted_token



# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer, FileUploadSerializer
from .models import FileUpload
from .utils import generate_encrypted_url





class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate secure link
            encrypted_url = generate_encrypted_url(user.email)
            verify_link = f"http://127.0.0.1:8000/api/verify-email/{encrypted_url}"

            return Response({
                "message": "Signup successful",
                "verify_url": verify_link
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
    def get(self, request, token):
        email = decode_encrypted_token(token)

        if email == "expired":
            return Response({"message": "Link expired!"}, status=status.HTTP_400_BAD_REQUEST)
        elif email == "invalid":
            return Response({"message": "Invalid verification link!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            if user.email_verified:
                return Response({"message": "Email already verified!"})
            user.email_verified = True
            user.save()
            return Response({"message": "Email verification successful!"})
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                "message": "Login successful",
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # ✅ Check user is 'ops'
        if request.user.user_type != 'ops':
            return Response({"error": "Only Ops user can upload files."}, status=403)

        # ✅ Check file type
        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return Response({"error": "No file provided."}, status=400)

        allowed_types = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
                         'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # pptx
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']  # xlsx

        if uploaded_file.content_type not in allowed_types:
            return Response({"error": "Only .docx, .pptx, .xlsx allowed."}, status=400)

        # ✅ Save file
        file_instance = FileUpload.objects.create(user=request.user, file=uploaded_file)
        serializer = FileUploadSerializer(file_instance)
        return Response(serializer.data, status=201)
    


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.email_verified:
            return Response({"error": "Email not verified"}, status=403)

        # ✅ Generate token or get existing one
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type
        })
