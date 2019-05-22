from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('create/', views.AuctionCreate.as_view(), name='auction-create'),
    path('', views.AuctionList.as_view(), name='auction-list')
]
