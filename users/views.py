from datetime import datetime
from random import randint

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config import settings
from users.models import PasswordResets
from users.permissions import IsOwnerOrSuperUser
from users.serializers import UserSerializer, ProfileSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class ProfileUpdateView(ModelViewSet):
    queryset = get_user_model().objects.all()
    allowed_methods = ('GET', 'PUT', 'PATCH', 'DELETE')
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrSuperUser,)


@api_view(['POST'])
def password_change_view(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fail'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            data={'status': 'fail', 'description': 'Only POST methods allowed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'POST'])
def password_reset_view(request):
    if request.method == 'POST':
        reset_code = request.data['code']
        new_password = request.data['new_password']
        try:
            reset_user = PasswordResets.objects.get(reset_code=reset_code, status=True)
            if datetime.now().timestamp() - reset_user.created_at.timestamp() > 600:
                # return time out error if code sent more than 10 minutes ago
                return Response({'status': 'fail', 'description': 'Code time out'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 'fail', 'description': 'Code invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = get_user_model().objects.get(pk=int(reset_user.user_id))
            PasswordResets.objects.filter(reset_code=reset_code).update(status=False)
            user.set_password(new_password)
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'fail', 'description': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        email = request.data['email']
        user = get_user_model().objects.filter(email=email).first()
        if user:
            reset_code = f"{randint(100, 999)}-{randint(100, 999)}"
            try:
                reset_request = PasswordResets.objects.create(user=user, reset_code=reset_code)
                reset_request.save()
                send_mail(
                    subject='Password Reset Request',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    message=f'Please, insert this code to reset your password: {reset_code}!\n\n'
                            f'Code will expire in 10 minutes.',
                )
                return Response(
                    data={'status': 'Code for reset your password sent to your email, check your email, please!'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                print(e)
                return Response({'status': 'fail'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                data={'status': 'fail', 'desctiption': 'email not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
