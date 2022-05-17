from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Person, User, ResetPasswordToken
from .serializers import *

from django.template.loader import render_to_string

class IsActivatedAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['email'])

        return Response(
            data={'is_active': user.is_active},
            status=status.HTTP_200_OK
        )


class SignUpAPIView(GenericAPIView):
    queryset = Person.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_activation_email()

        return Response(
            data={'detail': _('Check your email for confirmation link')},
            status=200
        )


class ActivateAPIView(GenericAPIView):

    def get(self, request, eid, token):
        User.activate(eid, token)
        response = HttpResponse('user/user_email_activated_callback.html')
        return response


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data={'data': serializer.data},
                        status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LogoutAPIView(GenericAPIView):
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ResendActivationEmailAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User,
                                     email=serializer.validated_data['email'])
            user.send_activation_email()
            return Response(
                data={'detail': _('Check your email for confirmation link')},
                status=200
            )


class PersonAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        user = request.user
        data = self.get_serializer(instance=user.person).data
        return Response(data={'data': data,
                              'token': Token.objects.get(user=user)},
                        status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = PersonSerializer(instance=user.person,
                                      data=request.data,
                                      partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'data': serializer.data},
            status=status.HTTP_200_OK
        )


class ChangePasswordAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'detail': _('password changed successfully')},
            status=200
        )


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data

        user = get_object_or_404(User, email=data['email'])
        user.send_password_confirm_email()

        return Response(
            {'detail': _('Successfully Sent Reset Password Email')},
            status=200)


class ResetPasswordConfirmAPIView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rs_token = get_object_or_404(ResetPasswordToken, uid=data['uid'],
                                     token=data['token'])
        if (timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User,
                                 id=urlsafe_base64_decode(data['uid']).decode('utf-8'))
        rs_token.delete()
        user.password = make_password(data['new_password1'])
        user.save()
        return Response(data={'detail': _('Successfully Changed Password')},
                        status=200)
