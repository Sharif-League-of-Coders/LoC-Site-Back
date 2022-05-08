from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.user.serializers import PersonWithTeamSerializer
from .models import Team, Invitation
from ..user.models import User
from .exceptions import *


class MemberSerializer(serializers.ModelSerializer):
    person = PersonWithTeamSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id', 'person']


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'members', 'creator', ]

    def create(self, data):
        current_user = self.context['request'].user
        data['creator'] = current_user

        team = Team.objects.create(**data)

        current_user.team = team
        current_user.save()
        return team


class TeamInfoSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'creator', 'members', 'id', ]


class TeamToUserInvitationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['user', 'status', ]

    def create(self, data):
        current_user = self.context['request'].user
        data['team'] = current_user.team
        data['type'] = 'team_to_user'
        data['user'] = get_object_or_404(User,
                                         email=self.context['request'].data[
                                             'user_email'])
        invitation = Invitation.objects.create(**data)
        return invitation

    def validate(self, data):
        request = self.context['request']
        target_user = get_object_or_404(User, email=request.data['user_email'])
        if request.user.team.is_complete():
            raise TeamIsFullException()
        elif target_user.team is not None:
            raise HasTeamException()
        elif Invitation.objects.filter(team=request.user.team,
                                       user=target_user,
                                       status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


class UserReceivedInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        invitation = get_object_or_404(Invitation,
                                       id=self.context['invitation_id'])
        answer = request.query_params.get('answer', "0")

        if request.user != invitation.user:
            raise PermissionDenied('this is not your invitation to change')
        elif answer == '1':
            if invitation.team.is_complete():
                raise TeamIsFullException()
            data['status'] = 'accepted'
        elif answer == '0':
            data['status'] = 'rejected'
        return data

    class Meta:
        model = Invitation
        fields = ['team', 'status', 'id']
