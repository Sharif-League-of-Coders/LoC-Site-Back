from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from rest_framework.authtoken.models import Token


class User(AbstractUser):
    team = models.ForeignKey(to='team.Team',
                             on_delete=models.CASCADE,
                             related_name='members', null=True, blank=True)

    def send_activation_email(self):
        activate_user_token = ActivateUserToken(
            token=Token.objects.create(user=self),
            eid=urlsafe_base64_encode(force_bytes(self.email)),
        )
        activate_user_token.save()

        context = {
            'domain': settings.DOMAIN,
            'eid': activate_user_token.eid,
            'token': activate_user_token.token,
        }

        from django.core.mail.message import EmailMultiAlternatives
        from django.core.mail import DEFAULT_ATTACHMENT_MIME_TYPE
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags

        email_message_html = render_to_string('user/user_activate_email.html',
                                              context=context)
        email_message_plaintext = strip_tags(email_message_html)

        email = EmailMultiAlternatives(
            subject='فعالساری اکانت LoC',
            body=email_message_plaintext,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.email]
        )

        email.attach_alternative(email_message_html, 'txt/html')
        email.send()

    def send_password_confirm_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.id))
        ResetPasswordToken.objects.filter(uid=uid).delete()
        reset_password_token = ResetPasswordToken(
            uid=uid,
            token=Token.objects.create(user=self),
            expiration_date=timezone.now() + timezone.timedelta(hours=24),
        )
        reset_password_token.save()
        context = {
            'domain': settings.DOMAIN,
            'username': self.username,
            'uid': reset_password_token.uid,
            'token': reset_password_token.token,
        }

        from django.core.mail.message import EmailMultiAlternatives
        from django.core.mail import DEFAULT_ATTACHMENT_MIME_TYPE
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags

        email_message_html = render_to_string('user/user_reset_password.html',
                                              context=context)
        email_message_plaintext = strip_tags(email_message_html)

        email = EmailMultiAlternatives(
            subject='تغییر رمزعبور LoC',
            body=email_message_plaintext,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.email]
        )

        email.attach_alternative(email_message_html, 'html')
        email.send()

    @classmethod
    def activate(cls, eid, token):
        activate_user_token = get_object_or_404(ActivateUserToken,
                                                eid=eid, token=token)

        email = urlsafe_base64_decode(eid).decode('utf-8')
        user = cls.objects.get(email=email)
        user.is_active = True
        activate_user_token.delete()
        user.save()


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='person')
    firstname = models.CharField(max_length=64, null=True)
    lastname = models.CharField(max_length=64, null=True)
    birthdate = models.DateField(null=True)
    university = models.CharField(max_length=64, null=True)
    phonenumber = models.CharField(max_length=32, null=True)
    stu_number = models.CharField(max_length=16, null=True)

    @property
    def is_complete(self):
        return all(
            (
                self.phonenumber, self.birthdate, self.firstname,
                self.lastname, self.university
            )
        )


class ActivateUserToken(models.Model):
    token = models.CharField(max_length=100)
    eid = models.CharField(max_length=100, null=True)


class ResetPasswordToken(models.Model):
    uid = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()
