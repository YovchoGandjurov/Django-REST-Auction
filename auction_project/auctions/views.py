from django.shortcuts import render
from rest_framework import generics

from .models import Auction, Category
from .serializers import CreateAuctionSerializer


class AuctionCreate(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = CreateAuctionSerializer


class AuctionList(generics.ListCreateAPIView):
    pass