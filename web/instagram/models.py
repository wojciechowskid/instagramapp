from django.db import models


class InstagramAccount(models.Model):

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    inst_user_id = models.CharField(max_length=255)

    long_lived_token = models.CharField(max_length=255)
    expires_in = models.DateTimeField()
