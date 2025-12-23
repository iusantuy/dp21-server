from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.middleware.csrf import get_token
from ..presentation.serializers import LoginSerializer, UserSerializer

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view  #   ✅ benar

# @method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]  # <--- ini penting
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response({"user": UserSerializer(user).data}, status=status.HTTP_200_OK)


# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         login(request, user)
#         return Response({"user": UserSerializer(user).data}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message": "Logout berhasil"}, status=status.HTTP_200_OK)



class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# user/views.py
@api_view(["GET"])
@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})











# from django.shortcuts import render

# # Create your views here.
# # users/presentation/views.py
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer

# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data

#         refresh = RefreshToken.for_user(user)
#         data = {
#             "user": UserSerializer(user).data,
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#         }
#         return Response(data, status=status.HTTP_200_OK)
