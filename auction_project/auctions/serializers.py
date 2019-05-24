from .models import Auction, Category
from rest_framework import serializers
import datetime

from accounts.models import Profile
from accounts.serializers import ProfileSerializer


class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('title', 'description', 'initial_price', 'closing_data',
                  'step', 'category', 'owner')
        read_only_fields = ('current_price', 'number_of_bits', 'created_at',
                            'status', 'owner', 'winner', 'participants')

    def create(self, validated_data):
        curr_user = Profile.objects.get(
            user_id=self.context['request'].user.id
        )
        validated_data['owner'] = curr_user
        validated_data['current_price'] = validated_data['initial_price']
        instance = Auction.objects.create(**validated_data)
        return instance


class AuctionListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ('id', 'title', 'initial_price', 'current_price',
                  'number_of_bids', 'closing_data', 'step', 'status',
                  'category', 'owner', 'winner', 'participants')
        # depth = 1

    def get_owner(self, obj):
        profile = Profile.objects.get(id=obj.owner.id)
        serializer = ProfileSerializer(profile)
        return serializer.data

    def get_winner(self, obj):
        if obj.winner is not None:
            profile = Profile.objects.get(id=obj.winner.id)
            serializer = ProfileSerializer(profile)
            return serializer.data
        return None

    def get_participants(self, obj):
        if obj.participants.count() > 0:
            result = []
            for x in range(obj.participants.count()):
                serializer = ProfileSerializer(obj.participants.all()[x])
                result.append(serializer.data)
            return result
        return None


class AuctionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('title', 'description', 'initial_price', 'closing_data',
                  'step', 'owner')
        read_only_fields = ('current_price', 'number_of_bits', 'created_at',
                            'status', 'owner', 'winner', 'participants')


class AuctionBidListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('id', 'title', 'description', 'current_price',
                  'number_of_bids', 'step', 'closing_data', 'owner',
                  'winner', 'participants'
                  )
        # depth = 2


class AuctionBidSerializer(serializers.ModelSerializer):
    bid = serializers.IntegerField(write_only=True, min_value=0)

    class Meta:
        model = Auction
        fields = ('bid', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')
