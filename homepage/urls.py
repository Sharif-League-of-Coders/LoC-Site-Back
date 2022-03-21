from django.urls import path
from homepage.views import StaffView, HomePageStaffView

urlpatterns = [
    path('staff/all/', StaffView.as_view()),
    path('staff/', HomePageStaffView.as_view()),
]
