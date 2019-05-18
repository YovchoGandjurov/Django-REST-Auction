from django.shortcuts import render
from rest_framework import generics

from .serializers import ProfileCreateSerializer, ProfileUpdateSerializer
from .models import Profile


class ProfileCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
