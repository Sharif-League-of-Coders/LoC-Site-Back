from django.db import models

from apps.user.models import User


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(to=User,
                                on_delete=models.CASCADE,
                                related_name='created_teams')

    def is_complete(self):
        return self.members.count() == 3

    def member_count(self):
        return self.members.count()


class InvitationStatusTypes:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    TYPES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    )


class Invitation(models.Model):
    user = models.ForeignKey(User, related_name='invitations',
                             on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='invitations',
                             on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=InvitationStatusTypes.TYPES,
        default=InvitationStatusTypes.PENDING
    )
    type = models.CharField(
        max_length=50,
        default='team_to_user',
    )
