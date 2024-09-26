from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Branches, CustomUser, UserRoles, Roles, PasswordReset
from .serializers import (BranchesViewSerializer, CustomTokenObtainPairSerializer, UserRolesWriteSerializer, UserRolesReadSerializer, UserListSerializer,
                          RolesViewSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, UserRegisterSerializer, UserProfileUpdateSerializer,
                          UserUpdateSerializer)

User = get_user_model()

class BranchesViewSet(viewsets.ModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchesViewSerializer
    permission_classes = [IsAuthenticated]


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesViewSerializer
    permission_classes = [IsAuthenticated]


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "success": True,
                "message": "User created successfully",
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.filter(id=user.id)
        return queryset


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class PasswordResetRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                exist = PasswordReset.objects.filter(username=user).exists()
                if exist:
                    encoded_username = urlsafe_base64_encode(username.encode())
                    reset_link = f"/password-reset/{encoded_username}/"
                    return Response({"reset_link": reset_link}, status=status.HTTP_200_OK)
                PasswordReset.objects.create(username=user)
                encoded_username = urlsafe_base64_encode(username.encode())
                reset_link = f"/password-reset/{encoded_username}/"
                return Response({"reset_link": reset_link}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, encoded_username):
        try:
            username = urlsafe_base64_decode(encoded_username).decode()
            reset_request = PasswordReset.objects.filter(username__username=username, clicked=False)

            if not reset_request.exists():
                return Response({"status": "Invalid", "error": "Password reset request does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            reset_request = reset_request.first()
            reset_request.clicked = True
            reset_request.save()

            return Response({"status": "Valid"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"status": "Invalid", "error": "Invalid encoded username."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, encoded_username):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                username = urlsafe_base64_decode(encoded_username).decode()
                reset_request = PasswordReset.objects.filter(username__username=username, clicked=True).first()

                if not reset_request:
                    return Response({"status": "Invalid", "error": "Password reset request does not exist or has already been used."}, status=status.HTTP_400_BAD_REQUEST)

                user = CustomUser.objects.get(username=username)
                user.set_password(serializer.validated_data['password'])
                user.save()
                reset_request.delete()
                return Response({"status": "Password reset"}, status=status.HTTP_200_OK)
            except (CustomUser.DoesNotExist, ValueError):
                return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRolesView(viewsets.ModelViewSet):
    queryset = UserRoles.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return UserRolesWriteSerializer
        return UserRolesReadSerializer

