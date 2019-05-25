from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
    Created to use for Profile Serializer
    """
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name',
                  'last_name', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    """
    List and Create Serializer

    Extended Django User using 'source' for each needed field.
    Additional field 'first_last_name' that combines the first and
    last name.
    Validate username with 'Field-level validation' to be unique.
    Overriding 'create' method to create а user and profile.
    """
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', write_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name',
                                       write_only=True)
    last_name = serializers.CharField(source='user.last_name', write_only=True)
    first_last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'password', 'email', 'first_name',
                  'last_name', 'first_last_name', 'language', 'profile_image')

    def validate_username(self, value):
        check_user = User.objects.all().filter(username=value)
        if len(check_user) != 0:
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return value

    def get_first_last_name(self, obj):
        first_last_name = obj.user.first_name + " " + obj.user.last_name
        return first_last_name

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(),
                                     validated_data=user_data)
        user.set_password(user_data['password'])
        user.save()

        profile = Profile.objects.create(user=user, **validated_data)
        return profile


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Update Serializer

    Extended Django User using 'source' for each needed field.
    Additional field 'first_last_name' that combines the first and
    last name.
    Overriding 'update' method to change а user and profile.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    password = serializers.CharField(source='user.password',
                                     write_only=True,
                                     required=False)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name',
                                       write_only=True,
                                       required=False)
    last_name = serializers.CharField(source='user.last_name',
                                      write_only=True,
                                      required=False)
    first_last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'password', 'email', 'first_name',
                  'last_name', 'first_last_name', 'language', 'profile_image')

    def get_first_last_name(self, obj):
        first_last_name = obj.user.first_name + " " + obj.user.last_name
        return first_last_name

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data,
                                         partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.update(instance.user, user_data)

        if 'password' in user_data:
            instance.user.set_password(user_data['password'])
            instance.user.save()

        super(ProfileUpdateSerializer, self).update(instance, validated_data)
        return instance
