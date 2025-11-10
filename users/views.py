from rest_framework import generics, permissions
from .serializers import UserSignupSerializer


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]
