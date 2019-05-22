from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

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

    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('current_price', 'days_to_end')
    filterset_fields = ('created_at', )
    permission_classes = [AdminOrReadOnly, OpenAuctionsOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Auction.objects.all()
        return Auction.objects.all().filter(status='Open')
