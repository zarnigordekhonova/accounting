from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.serializers import UserSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


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
