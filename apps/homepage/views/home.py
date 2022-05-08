from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.homepage.models import Home
from apps.homepage.serializer import HomeSerializer


class HomeView(ListAPIView):
    queryset = Home.objects.filter(activate=True)
    serializer_class = HomeSerializer
#    permission_classes = [IsAuthenticated]
