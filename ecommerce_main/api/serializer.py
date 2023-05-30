from api.models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    get_images = serializers.Field()
    class Meta:
        model = Product
        depth = 1
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        depth = 1
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        depth = 1
        fields = "__all__"
