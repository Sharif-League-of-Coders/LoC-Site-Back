from rest_framework.generics import ListAPIView
from homepage.models import Home
from homepage.serializer import HomeSerializer


class HomeView(ListAPIView):
    queryset = Home.objects.filter(activate=True)
    serializer_class = HomeSerializer
