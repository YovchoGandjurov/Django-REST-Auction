from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Auction, Category
from .serializers import AuctionCreateSerializer, AuctionListSerializer, \
                         AuctionUpdateSerializer
from .method_serializer_view import MethodSerializerView
from .permissions import AdminOrReadOnly, IsOwnerOrAdmin

from accounts.models import Profile


class AuctionCreate(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuctionList(MethodSerializerView, generics.ListCreateAPIView):
    method_serializer_classes = {
        ('GET'): AuctionListSerializer,
        ('POST'): AuctionCreateSerializer
    }

    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('current_price', 'days_to_end')
    filterset_fields = ('created_at', )
    permission_classes = [AdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Auction.objects.all()
        return Auction.objects.all().filter(status='Open')


class AuctionListByUser(generics.ListAPIView):
    serializer_class = AuctionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user__id=self.request.user.id)
        return Auction.objects.all().filter(owner_id=profile.id)


class AuctionUpdate(
        MethodSerializerView, generics.RetrieveUpdateDestroyAPIView
        ):
    method_serializer_classes = {
        ('GET', ): AuctionListSerializer,
        ('PUT', 'PATCH'): AuctionUpdateSerializer
    }
    queryset = Auction.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
