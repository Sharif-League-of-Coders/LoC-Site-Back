from rest_framework import serializers
from apps.homepage.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Staff
        fields = ['name', 'image', 'position']

    def get_image(self, instance):
        return instance.image.url
