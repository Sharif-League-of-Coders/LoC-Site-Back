from rest_framework import serializers
from apps.homepage.models import Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sponsor
        fields = ['name', 'logo', 'website_address']

    def get_logo(self, instance):
        return instance.logo.url
