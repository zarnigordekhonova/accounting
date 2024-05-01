from rest_framework.generics import CreateAPIView

from users.serializers import UserSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
