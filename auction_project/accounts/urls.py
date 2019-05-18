from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('register/', views.ProfileCreate.as_view(), name='register'),
    re_path('(?P<pk>\d+)/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('', include('rest_auth.urls')),
]
