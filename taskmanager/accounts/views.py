from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, LogoutSerializer
)
from django.core.exceptions import ValidationError  
        
class RegisterAPIView(APIView):
    def post(self, request):
        try:
            print("Requested data=====",request.data)
            email = request.data.get('email')
            name = request.data.get('name')
            password = request.data.get('password')
            
            if User.objects.filter(email=email).exists():
                print("Emial Already exist")
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                print("Serializer Error=====",serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
            # Create user
            User.objects.create_user(
                email=email,
                name=name,
                password=password,
                  
            )
           
            return Response(
                {"success": "User created successfully."},
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            print("Validation error",e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected Error:", str(e))
            return Response(
                {"error": "Something went wrong. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

  
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": "Invalid login credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        print("Last Step for login")
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "Login successful"
        })



class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            refresh_token = serializer.validated_data["refresh"]

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=200)

        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=400)

        except Exception as e:
            print("Logout Error:", str(e))
            return Response({"error": "Something went wrong"}, status=500)
