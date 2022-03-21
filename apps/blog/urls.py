from django.urls import path

from . import views

urlpatterns = [

    path('', view=views.PostsAPIView.as_view(), name='posts'),
    path('<int:post_id>', view=views.PostAPIView.as_view(), name='post'),
]