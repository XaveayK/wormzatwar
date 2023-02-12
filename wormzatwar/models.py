from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

class WormUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, null=False)

class country():
    name = models.CharField()
    occupier = models.ForeignKey(WormUser, on_delete=models.SET_NULL, null=True, default=None, related_name='users')
    gucci = models.IntegerField()
    food = models.IntegerField()

class Lobby(models.Model):

    lobbyPK = models.CharField(
        max_length=6, 
        primary_key=True,
        editable=False,
        unique=True)

    def save(self, *args, **kwargs):
        if not self.lobbyPK:
            self.lobbyPK = get_random_string(6)
        return super(Lobby, self).save(*args, **kwargs)
    
    wormuser = models.ManyToManyField(WormUser)
    owner = models.ForeignKey(WormUser, on_delete=models.CASCADE, null=False, default=None, related_name='owner')