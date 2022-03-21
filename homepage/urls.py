from django.urls import path
from homepage.views import StaffView, HomePageStaffView, SponsorView, HomeView

urlpatterns = [
    path('staff/all/', StaffView.as_view()),
    path('staff/', HomePageStaffView.as_view()),
    path('sponsor/', SponsorView.as_view()),
    path('home/', HomeView.as_view()),
]
