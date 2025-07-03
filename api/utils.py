from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

def generate_encrypted_url(email):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    return s.dumps(email, salt='email-confirm')

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

        # ✅ Token create or fetch
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key,
            "username": user.username,
            "user_type": user.user_type
        })