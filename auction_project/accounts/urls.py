from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.ProfileList.as_view(), name='all-users'),
    re_path('(?P<pk>\d+)/', views.ProfileDetail.as_view(), name='profile'),
    path('register/', views.ProfileCreate.as_view(), name='register'),
    path('auth/', include('rest_framework.urls')),
]
