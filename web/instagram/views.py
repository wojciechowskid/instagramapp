from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def view(request):
    """Just a handy view for getting auth_code from instagram"""

    app_id = settings.INSTAGRAM_APP_ID
    secret = settings.INSTAGRAM_SECRET
    redirect_uri = settings.INSTAGRAM_REDIRECT_URI

    if not app_id or not secret:
        return HttpResponse('Configure correct Instagram App Id and Secret')

    url = f"https://api.instagram.com/oauth/authorize?client_id={app_id}"+\
    f"&redirect_uri={redirect_uri}&scope=user_profile,user_media"+\
    "&response_type=code"

    html = f"""
        <html>
            <body>
            <a href={url}>Authorize the App and get Authorization code</a>
            </body>
        </html>"""
    return HttpResponse(html)
