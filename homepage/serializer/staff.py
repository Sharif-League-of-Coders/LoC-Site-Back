from rest_framework import serializers
from homepage.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['name', 'image', 'position']
