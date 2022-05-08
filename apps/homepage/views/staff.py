from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.homepage.models import Staff
from apps.homepage.serializer import StaffSerializer


class StaffView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
#    permission_classes = [IsAuthenticated]


class HomePageStaffView(ListAPIView):
    queryset = Staff.objects.filter(show_in_homepage=True)
    serializer_class = StaffSerializer
#    permission_classes = [IsAuthenticated]
