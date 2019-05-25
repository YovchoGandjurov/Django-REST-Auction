from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from .serializers import ProfileSerializer, ProfileUpdateSerializer
from .models import Profile
from .permissions import IsNotAuthenticated, IsOwnerOrAdmin


class ProfileCreate(generics.CreateAPIView):
    """
    Create Profile. Only for unauthorized users or admins/superusers. 
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsNotAuthenticated]


class ProfileList(generics.ListCreateAPIView):
    """
    List and Create Profile. Only for admin users.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update and Delete.
    Only for authorized users, owners or admins/superusers.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
