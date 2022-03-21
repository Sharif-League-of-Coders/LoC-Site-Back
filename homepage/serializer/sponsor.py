from rest_framework import serializers
from homepage.models import Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['name', 'logo', 'website_address']
