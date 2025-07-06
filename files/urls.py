from django.urls import path
from .views import FileUploadView, list_uploaded_files, delete_file
from . import views

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('list/', list_uploaded_files),   # 👈 Add this
    path('download/<int:file_id>/', views.generate_download_link, name='generate_download_link'),
    path('download/secure/<str:token>/', views.secure_file_download, name='secure_file_download'),
    path('files/delete/<int:file_id>/', delete_file),




]
