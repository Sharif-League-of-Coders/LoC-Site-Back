from rest_framework import serializers
from homepage.models import Home


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['about_this_event', ]
