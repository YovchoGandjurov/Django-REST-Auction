from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .serializers import ProfileCreateSerializer, ProfileUpdateSerializer
from .models import Profile

from .permissions import IsNotAuthenticated, IsOwnerOrAdmin


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class ProfileCreate(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsNotAuthenticated]
