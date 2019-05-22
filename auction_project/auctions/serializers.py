from .models import Auction
from rest_framework import serializers

from accounts.models import Profile
# from accounts.serializers import ProfileSerializer


class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('title', 'description', 'initial_price', 'days_to_end',
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
        exclude = []
        depth = 2


class AuctionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ('title', 'description', 'initial_price', 'days_to_end',
                  'step', 'owner')
        read_only_fields = ('current_price', 'number_of_bits', 'created_at',
                            'status', 'owner', 'winner', 'participants')
