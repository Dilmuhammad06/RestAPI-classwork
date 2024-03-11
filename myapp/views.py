from django.shortcuts import render
from .serializers import SignUp
from rest_framework.generics import CreateAPIView
from .models import User


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUp