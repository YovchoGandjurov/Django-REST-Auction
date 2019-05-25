from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS
from datetime import date

from .models import Auction, Category
from .serializers import AuctionCreateSerializer, AuctionListSerializer, \
                         AuctionUpdateSerializer, AuctionBidSerializer, \
                         CategorySerializer
from .permissions import AdminOrReadOnly, IsOwnerOrAdmin

from accounts.models import Profile


class AuctionCreate(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuctionList(generics.ListCreateAPIView):
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('current_price', 'closing_data')
    filterset_fields = ('closing_data', 'current_price')
    permission_classes = [AdminOrReadOnly]

    @staticmethod
    def check_date(end_date):
        return date.today() > end_date

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuctionListSerializer
        return AuctionCreateSerializer

    def get_queryset(self):
        for obj in Auction.objects.all():
            if self.check_date(obj.closing_data):
                obj.status = 'Closed'
                obj.save()

        if self.request.user.is_staff or self.request.user.is_superuser:
            return Auction.objects.all()
        return Auction.objects.all().filter(status='Open')


class AuctionListByUser(generics.ListAPIView):
    serializer_class = AuctionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = Profile.objects.get(user__id=self.request.user.id)
        return Auction.objects.all().filter(owner_id=profile.id)


class AuctionUpdate(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuctionListSerializer
        return AuctionUpdateSerializer

    queryset = Auction.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class AuctionBid(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuctionListSerializer
        return AuctionBidSerializer

    def list(self, request, pk):
        queryset = Auction.objects.all().filter(id=pk)
        serializer = AuctionListSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        bid = request.data['bid']
        current_profile = Profile.objects.get(user__id=self.request.user.id)

        if not str(bid).isdigit():
            raise serializers.ValidationError("The value must be a digit.")
        if bid < instance.step:
            raise serializers.ValidationError(
                "The bid must be greater than or equal to step."
            )

        instance.number_of_bids = instance.number_of_bids + 1
        instance.current_price = instance.current_price + bid
        instance.winner = current_profile
        instance.participants.add(current_profile)
        instance.save()

        return self.list(request, instance.id)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
