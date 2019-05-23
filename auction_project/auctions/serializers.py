from .models import Auction
from rest_framework import serializers
import datetime

from accounts.models import Profile


class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('title', 'description', 'initial_price', 'closing_data',
                  'step', 'owner')
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

    class Meta:
        model = Auction
        fields = '__all__'
        # exclude = []
        depth = 2


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
