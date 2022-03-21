from rest_framework.generics import ListAPIView
from homepage.models import Staff
from homepage.serializer import StaffSerializer


class StaffView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class HomePageStaffView(ListAPIView):
    queryset = Staff.objects.filter(show_in_homepage=True)
    serializer_class = StaffSerializer
