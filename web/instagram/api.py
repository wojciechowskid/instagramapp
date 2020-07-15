from rest_framework.decorators import api_view
from .serializers import AuthCodeSerializer, InstagramAccountSerializer
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from .models import InstagramAccount
from datetime import timedelta
from django.utils import timezone


class CreateInstagramAccountViewSet(mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    queryset = InstagramAccount.objects.all()
    serializer_class = AuthCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_code = serializer.validated_data['auth_code']
        user_id = self.kwargs.get('user_id')

        sresponse = self.get_short_lived_token(auth_code)
        if sresponse.get('error_type'):
            return Response(sresponse, status=status.HTTP_400_BAD_REQUEST)

        lresponse = self.get_long_lived_token(sresponse.get('access_token'))
        if lresponse.get('error'):
            return Response(lresponse.get('error'),
                status=status.HTTP_400_BAD_REQUEST)

        model_serializer = InstagramAccountSerializer(data={
            'user': user_id,
            'inst_user_id': sresponse.get('user_id'),
            'long_lived_token': lresponse.get('access_token'),
            'expires_in': timezone.now() + \
            timedelta(seconds=lresponse.get('expires_in'))
        })

        if model_serializer.is_valid():
            self.perform_create(model_serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(model_serializer.data,
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(model_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def get_short_lived_token(self, auth_code):
        """exchanges auth_code for short lived token"""

        r = requests.post(settings.INSTAGRAM_STOKEN_URI, {
            'client_id': settings.INSTAGRAM_APP_ID,
            'client_secret': settings.INSTAGRAM_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.INSTAGRAM_REDIRECT_URI,
            'code': auth_code
        })

        return r.json()

    def get_long_lived_token(self, short_lived_token):
        """a method to exchange `short_lived_token` for long lived one"""

        uri = settings.INSTAGRAM_ROOT_URI + '/access_token'

        r = requests.get(uri, {
            'client_secret': settings.INSTAGRAM_SECRET,
            'access_token': short_lived_token,
            'grant_type': 'ig_exchange_token'
        })

        return r.json()
