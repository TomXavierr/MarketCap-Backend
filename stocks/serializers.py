from rest_framework import serializers
from  .models import Stock, Watchlist

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'symbol']

    def create(self, validated_data):
        return Stock.objects.create(**validated_data)


class StockInfoSerializer(serializers.Serializer):
    Name = serializers.CharField()
    open = serializers.CharField()
    high = serializers.CharField()
    low = serializers.CharField()
    close = serializers.CharField()

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'stocks']

    def create(self, validated_data):
        user = self.context['request'].user
        watchlist, created = Watchlist.objects.get_or_create(user=user, defaults={})
        return watchlist

class TickerSearchSerializer(serializers.Serializer):
    keywords = serializers.CharField(max_length=255)