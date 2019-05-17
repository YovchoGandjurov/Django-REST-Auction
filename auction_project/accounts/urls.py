from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('register/', views.ProfileCreate.as_view(), name='register'),
    path('', include('rest_auth.urls')),
]
