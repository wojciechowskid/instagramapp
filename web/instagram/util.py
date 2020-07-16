import requests
from django.conf import settings
import base64, hmac, json, hashlib


class Instagram:

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

    def get_recent_images(self, token, length=10):
        uri = settings.INSTAGRAM_ROOT_URI + '/me/media'
        media = requests.get(uri,{
            "fields": 'id,media_url,timestamp, media_type',
            "access_token": token
        })

        imgs = media.json().get('data')
        if not imgs:
            return imgs
        imgs = imgs[:length]
        albums = filter(lambda img: img['media_type'] == 'CAROUSEL_ALBUM', imgs)
        imgs = list(filter(lambda img: img['media_type'] != 'CAROUSEL_ALBUM', imgs))

        for album in albums:
            uri = settings.INSTAGRAM_ROOT_URI + '/' + album.get('id') + '/children'
            child_imgs = requests.get(uri, {
                "fields": "id,media_url,timestamp,media_type",
                "access_token": token
            })
            imgs += child_imgs.json().get('data')

        imgs = sorted(imgs, key=lambda img: img['timestamp'], reverse=True)
        return imgs[:length]

    def parse_signed_request(self, signed_request):
        secret = settings.INSTAGRAM_SECRET

        if not signed_request:
            raise ValueError('Ivalid Signed Request!')

        encoded_sig, payload = signed_request.split('.', 2)

        sig = self.base64_url_decode(encoded_sig)
        data = json.loads(self.base64_url_decode(payload))

        if data.get('algorithm').upper() != 'HMAC-SHA256':
            raise ValueError('Unsupported algorithm')

        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

        if sig != expected_sig:
            raise ValueError('Bad Signed JSON signature!')

    def base64_url_decode(self, inp):
        padding_factor = (4 - len(inp) % 4)
        inp += "="*padding_factor
        return base64.urlsafe_b64decode(inp)
