from rest_framework.decorators import api_view
from .serializers import AuthCodeSerializer, InstagramAccountSerializer
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from .models import InstagramAccount
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from .util import Instagram
from rest_framework.decorators import api_view


class CreateInstagramAccountViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    queryset = InstagramAccount.objects.all()
    serializer_class = AuthCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_code = serializer.validated_data['auth_code']
        user_id = self.kwargs.get('user_id')

        inst = Instagram()
        sresponse = inst.get_short_lived_token(auth_code)
        if sresponse.get('error_type'):
            return Response(sresponse, status=status.HTTP_400_BAD_REQUEST)

        lresponse = inst.get_long_lived_token(sresponse.get('access_token'))
        if lresponse.get('error'):
            return Response(lresponse.get('error'),
                status=status.HTTP_400_BAD_REQUEST)

        model_serializer = InstagramAccountSerializer(data={
            'user': user_id,
            'inst_user_id': sresponse['user_id'],
            'long_lived_token': lresponse['access_token'],
            'expires_in': timezone.now() + \
            timedelta(seconds=lresponse['expires_in'])
        })

        if model_serializer.is_valid():
            self.perform_create(model_serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(model_serializer.data,
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(model_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwrags):
        user_id = self.kwargs.get('user_id')
        account = get_object_or_404(InstagramAccount, pk=user_id)
        token = account.long_lived_token
        inst = Instagram()
        imgs = inst.get_recent_images(token)

        return Response(imgs, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        instance = get_object_or_404(InstagramAccount, pk=user_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def delete_data(request):
    if request.method == 'POST':
        signed_data = request.data.get('signed_data')

        inst = Instagram()
        try:
            data = inst.parse_signed_request(signed_request)
            user_id = data.get('user_id')
            accounts = InstagramAccount.objects.filter(inst_user_id=user_id)
            for account in accounts:
                account.delete()
        except (ValueError, KeyError) as err:
            return Response({'error': err},
                            status=status.HTTP_400_BAD_REQUEST)
        except InstagramAccount.DoesNotExists:
            pass
        return Response({'url': 'http://deleted.com',
                         'confirmation_code': 'the user data deleted'})
    return Response({'error': 'Unsupported method'},
                    status=status.HTTP_400_BAD_REQUEST)
