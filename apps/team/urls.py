from django.urls import path

from apps.team.views import *

urlpatterns = [
    path('', view=TeamAPIView.as_view(), name="team_operations"),
    path('invitations/user_pending',
         view=UserReceivedPendingInvitationListAPIView.as_view(),
         name="get_user_received_pending_invitations"),
    path('invitations/history',
         view=UserReceivedResolvedInvitationListAPIView.as_view(),
         name="get_user_received_resolved_invitations"),
    path('invitations/user_pending/<str:invitation_id>',
         view=UserAnswerInvitationAPIView.as_view(),
         name="user_answer_invitation"),
    path('invitations/team_sent', view=TeamSentInvitationListAPIView.as_view(),
         name="team_sent_invitation_list"),
    path('<str:team_id>', view=TeamInfoAPIView.as_view(), name="get_team"),
]
