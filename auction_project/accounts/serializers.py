from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'profile_image', 'language')

    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        profile = ProfileSerializer.objects.create(user=user, **validated_data)
