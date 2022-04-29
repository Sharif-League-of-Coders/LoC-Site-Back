from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.homepage.models import Sponsor
from apps.homepage.serializer import SponsorSerializer


class SponsorView(ListAPIView):
    queryset = Sponsor.objects.filter(activated_for_this_event=True)
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated, ]
