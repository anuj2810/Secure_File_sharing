from django.urls import path
from .views import SignupView, VerifyEmailView, CustomLoginView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('verify/<str:encoded_id>/', VerifyEmailView.as_view()),
    path('api/login/', CustomLoginView.as_view(), name='custom_login'),

]


