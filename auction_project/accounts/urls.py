from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.ProfileList.as_view(), name='all-users'),
    path('register/', views.ProfileCreate.as_view(), name='register'),
    re_path('(?P<pk>\d+)/', views.ProfileDetail.as_view(), name='profile'),
    path('auth/', include('rest_framework.urls')),
]
