from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UploadedFileSerializer
from .models import UploadedFile
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import jwt
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile
import jwt
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile

# ======================================================================================================================================

# class FileUploadView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user

#         # ✅ Check if user is "ops"
#         if user.user_type != 'ops':
#             return Response({'error': 'Only ops user can upload files.'}, status=403)

#         # ✅ Check file extension
#         uploaded_file = request.FILES.get('file')
#         if not uploaded_file:
#             return Response({'error': 'No file provided.'}, status=400)

#         allowed_extensions = ['pptx', 'docx', 'xlsx','pdf']
#         ext = uploaded_file.name.split('.')[-1]
#         if ext not in allowed_extensions:
#             return Response({'error': 'Invalid file type.'}, status=400)

#         # ✅ Save file
#         serializer = UploadedFileSerializer(data={'file': uploaded_file})
#         if serializer.is_valid():
#             serializer.save(uploader=user)
#             return Response({
#                 'message': 'File uploaded successfully',
#                 "id": uploaded_file.id
#                 }, status=201)
#         return Response(serializer.errors, status=400)

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        # ✅ Only ops can upload
        if user.user_type != 'ops':
            return Response({'error': 'Only ops user can upload files.'}, status=403)

        # ✅ File existence and extension check
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'error': 'No file provided.'}, status=400)

        allowed_extensions = ['pptx', 'docx', 'xlsx', 'pdf']
        ext = uploaded_file.name.split('.')[-1]
        if ext not in allowed_extensions:
            return Response({'error': 'Invalid file type.'}, status=400)

        # ✅ Save file
        serializer = UploadedFileSerializer(data={'file': uploaded_file})
        if serializer.is_valid():
            saved_file = serializer.save(uploader=user)
            return Response({
                'message': 'File uploaded successfully',
                'id': saved_file.id
            }, status=201)
        return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_uploaded_files(request):

    user = request.user
    if user.user_type != 'client':
        return Response({'error': 'Only client users can view the files list.'}, status=status.HTTP_403_FORBIDDEN)
    
    files = UploadedFile.objects.all()
    serializer = UploadedFileSerializer(files, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_download_link(request, file_id):
    user = request.user
    if user.user_type != 'client':
        return JsonResponse({"error": "Only client user can access download links."}, status=403)

    try:
        file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        return JsonResponse({"error": "File not found."}, status=404)

    # generate secure token using JWT
    payload = {
        "file_id": file.id,
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=5),  # valid for 5 mins
        "type": "download"
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    # After creating the secure download URL
    download_url = f"http://127.0.0.1:8000/api/files/download/secure/{token}/"

    # Send email
    send_mail(
        subject='Your Secure File Download Link',
        message=f'Click the link below to download your file:\n{download_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )
    return JsonResponse({
        "download_link": download_url,
        "message": "success"
    })


# files/views.py



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_file_download(request, token):
    user = request.user

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return Response({
            "error": "Token expired",
            "message": "Token has expired. Please request a new secure download link."
        }, status=401)
    except jwt.InvalidTokenError:
        return Response({
            "error": "Invalid token",
            "message": "The token is invalid or tampered with."
        }, status=401)

    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid token"}, status=400)

    if user.user_type != 'client' or user.id != payload.get('user_id'):
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    file_id = payload.get('file_id')

    try:
        file = UploadedFile.objects.get(id=file_id)
    except UploadedFile.DoesNotExist:
        return JsonResponse({"error": "File not found"}, status=404)

    return FileResponse(file.file.open(), as_attachment=True)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, file_id):
    try:
        file_obj = UploadedFile.objects.get(id=file_id, user=request.user)
        file_obj.file.delete()  # deletes actual file from disk
        file_obj.delete()       # deletes db entry
        return Response({"message": "File deleted successfully"})
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found or permission denied"}, status=404)
