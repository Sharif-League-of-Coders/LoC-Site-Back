from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import GenericAPIView, get_object_or_404


from apps.user.permissions import PersonComplete
from .models import Team, Invitation
from .permissions import HasTeam, NoTeam
from .serializers import *


class TeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Team.objects.all()

    def get(self, request):
        team = request.user.team
        data = self.get_serializer(team).data

        return Response(data)

    def post(self, request):
        team = self.get_serializer(data=request.data)
        team.is_valid(raise_exception=True)
        team.save()
        # request.user.reject_all_pending_invites()
        return Response(
            data={
                "data": team.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request):
        team = self.get_serializer(data=request.data,
                                   instance=request.user.team, partial=True)
        team.is_valid(raise_exception=True)
        team.save()

        return Response(
            data={
                "data": team.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        current_user = request.user

        if current_user.team.member_count() == 1:
            current_user.team.delete()
        current_user.team = None
        current_user.save()

        return Response(
            data={"message": "You left the team"},
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        new_permissions = self.permission_classes.copy()
        if self.request.method in ['PUT', 'GET', 'DELETE']:
            new_permissions += [HasTeam]
        if self.request.method == 'POST':
            new_permissions += [NoTeam] # , PersonComplete
        return [permission() for permission in new_permissions]


class TeamInfoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get(self, req, team_id):
        team = get_object_or_404(Team, id=team_id)
        data = self.get_serializer(instance=team).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserReceivedPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 status='pending',
                                                 type='team_to_user')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserReceivedResolvedInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 type='team_to_user'
                                                 ).exclude(status="pending")
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserAnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, NoTeam]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.query_params.get('answer') == '1':
            user = invitation.user
            user.team = invitation.team
            invitation.save()
            user.save()
            # if (invitation.team.is_complete()):
            #     invitation.team.reject_all_pending_invitations()
            # user.reject_all_pending_invites()
        if request.query_params.get('reject') == '1':
            invitation.type = 'rejected_team_to_user'
            invitation.save()

        return Response(
            data={"detail": f"Invitation is {serializer.data['status']}"},
            status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['invitation_id'] = self.kwargs['invitation_id']
        return context


class TeamSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeamToUserInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(team=request.user.team,
                                                 type='team_to_user')
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        new_permissions = self.permission_classes.copy()
        if self.request.method == 'POST':
            new_permissions += [HasTeam]
        return [permission() for permission in new_permissions]
