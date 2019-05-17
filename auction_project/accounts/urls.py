from django.urls import path, re_path, include


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
