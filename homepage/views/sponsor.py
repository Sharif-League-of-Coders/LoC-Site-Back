from rest_framework.generics import ListAPIView
from homepage.models import Sponsor
from homepage.serializer import SponsorSerializer


class SponsorView(ListAPIView):
    queryset = Sponsor.objects.filter(activated_for_this_event=True)
    serializer_class = SponsorSerializer
