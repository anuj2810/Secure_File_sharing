from django.urls import path
from .views import SignupView, EmailVerifyView,LoginView, FileUploadView



urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/<str:token>/', EmailVerifyView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),  # 👈 Add this
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
