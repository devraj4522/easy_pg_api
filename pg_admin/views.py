from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from easy_pg_backend.users.models import User

from .models import EasyPgUser
from .serializers import EasyPgUserSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserLoginView(APIView):
    serializer_class = EasyPgUserSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response_dict = {
            "statusCode": "",
            "statusMessage": "",
        }

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = request.data["password"]

            try:
                user = User.objects.get(username=email)
            except:
                response_dict["statusCode"] = -1
                response_dict["statusMessage"] = "user not found with given credentials"
                return Response(response_dict)

            user = authenticate(request, username=user.username, password=password)
            user_serializer = EasyPgUserSerializer(user)
            if user is not None:
                token = user.auth_token
                easy_pg_user = EasyPgUser.objects.get(user=user.id)
                data = {
                    "auth": {
                        "user": user.username,
                        "token": token.key,
                        "user_id": easy_pg_user.id,
                    },
                    "user": user_serializer.data,
                }
                response_dict["statusCode"] = 0
                response_dict["statusMessage"] = "Login successfull"
                response_dict["data"] = data
                return Response(response_dict)
            else:
                response_dict["statusCode"] = -1
                response_dict["statusMessage"] = "Incorrect password, Login fail"
                return Response(response_dict)
        else:
            response_dict["statusCode"] = -1
            response_dict["statusMessage"] = "Invalid credentials, Login fail"
            return Response(response_dict)
