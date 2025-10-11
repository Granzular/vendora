from rest_framework import serializers
from .models import Cart,CartPosition

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"

class CartPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartPosition
        fields = ["product","quantity"]
