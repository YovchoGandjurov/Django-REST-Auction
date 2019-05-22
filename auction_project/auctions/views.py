from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions

from .models import Auction, Category
from .serializers import AuctionCreateSerializer, AuctionListSerializer
from .method_serializer_view import MethodSerializerView
from .permissions import AdminOrReadOnly, OpenAuctionsOrAdmin


class AuctionCreate(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuctionList(MethodSerializerView, generics.ListCreateAPIView):
    method_serializer_classes = {
        ('GET'): AuctionListSerializer,
        ('POST'): AuctionCreateSerializer
    }
    permission_classes = [AdminOrReadOnly, OpenAuctionsOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Auction.objects.all()
        return Auction.objects.all().filter(status='Open')
