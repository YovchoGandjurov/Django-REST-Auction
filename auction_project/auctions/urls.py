from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.AuctionList.as_view(), name='auction-list'),
    path('create/', views.AuctionCreate.as_view(), name='auction-create'),
    path('mine/', views.AuctionListByUser.as_view(), name='mine'),
    re_path('^(?P<pk>\d+)/edit/$', views.AuctionUpdate.as_view(),
            name='auction-edit'),
    re_path('^(?P<pk>\d+)/bid/$',
            views.AuctionBid.as_view({'get': 'list', 'patch': 'partial_update'}),
            name='auction-bid'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    re_path('^category/(?P<pk>\d+)/$', views.CategoryDetail.as_view(),
            name='category-detail')    
]
