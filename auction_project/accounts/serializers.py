from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('username', )


class ProfileCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=True)
    UserCreateSerializer.Meta.read_only_fields = ()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'profile_image', 'language')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer.create(UserCreateSerializer(),
                                           validated_data=user_data)
        user.set_password(user_data['password'])
        user.save()

        profile = Profile.objects.create(user=user, **validated_data)
        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'profile_image', 'language')
        read_only_fields = ('username', )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserUpdateSerializer(instance.user, data=user_data,
                                               partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.update(instance.user, user_data)

        instance.user.set_password(user_data['password'])

        super(ProfileUpdateSerializer, self).update(instance, validated_data)
        return instance
