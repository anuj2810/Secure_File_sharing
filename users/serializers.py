from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type='client',  # client hi signup karega
            is_active=False      # jab tak verify nahi karta, active nahi
        )
        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Optional: extra info token me add karna ho to yahan karo
        token['username'] = user.username
        token['user_type'] = user.user_type
        return token
