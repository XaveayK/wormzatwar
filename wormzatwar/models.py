from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class WormUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, null=False)

class Lobby(models.Model):

    lobbyPK = models.CharField(
        max_length=6, 
        primary_key=True,
        editable=False,
        unique=True)

    stage = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(4), MinValueValidator(1)]
    )

    def save(self, *args, **kwargs):
        if not self.lobbyPK:
            self.lobbyPK = get_random_string(6)
        return super(Lobby, self).save(*args, **kwargs)

    wormuser = models.ManyToManyField(WormUser, through='userInLobby')
    owner = models.ForeignKey(WormUser, on_delete=models.CASCADE, null=False, default=None, related_name='owner')

class country(models.Model):
    name = models.CharField(max_length=50)
    occupier = models.ForeignKey(WormUser, on_delete=models.SET_NULL, null=True, default=None, related_name='users')
    gucci = models.IntegerField()
    food = models.IntegerField()
    occupyingForce = models.IntegerField()
    troopGen = models.IntegerField()
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, null=False)
    color = models.CharField(max_length=10, null=True)

class userInLobby(models.Model):
    user = models.ForeignKey(WormUser, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)

    class Colors(models.TextChoices):
        RED = '1', _('Red')
        BLUE = '2', _('Blue')
        GREEN = '3', _('Green')


    color = models.CharField(choices=Colors.choices, max_length=10)