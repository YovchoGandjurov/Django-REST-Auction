from django.shortcuts import render
from rest_framework import generics

from .serializers import ProfileSerializer
from .models import Profile


class ProfileCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
