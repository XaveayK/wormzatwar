from django.shortcuts import render, redirect, HttpResponse
from .forms import newUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Lobby, WormUser, userInLobby, country
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.generic import TemplateView
from django.views import View
from .helpers import gameStage, acrToCountries, countriesToAcr
import json
import random

def gameLobby(request, lobbyID):
    lobby = Lobby.objects.get(lobbyPK=lobbyID)
    if lobby.wormuser.filter(pk = request.user.id).exists():
        return render(request, 'lobby.html', 
            {   
                'LobbyPK':lobbyID, 
                'Users':lobby.wormuser.all(),
                'Colors':userInLobby.Colors.labels,
                'CurrUser': request.user.username
            })
    else:
        if Lobby.objects.get(lobbyPK=lobbyID).stage == 1:
            lobby.wormuser.add(WormUser.objects.get(pk = request.user.id))
            return render(request, 'lobby.html', 
                {
                    'LobbyPK':lobbyID, 
                    'Users':lobby.wormuser.all(), 
                    'Colors':userInLobby.Colors.labels,
                    'CurrUser': request.user.username
                })
        else:
            return HttpResponseNotAllowed('<h3>Can not join a started game!</h3>')

class gameStatus(View):
    def get(self, request, lobbyID, *args, **kwargs):
        return HttpResponse(Lobby.objects.get(lobbyPK=lobbyID).stage, content_type="text/plain")

class startGame(View):
    def post(self, request, lobbyID, *args, **kwargs):
        lobby = Lobby.objects.filter(lobbyPK=lobbyID).update(stage=2)
        self.getCountries(lobbyID)
        return HttpResponse("You did it!", content_type="text/plain")
    
    def getCountries(self, lobbyID):
        users = userInLobby.objects.filter(lobby_id=lobbyID).values_list('user_id', flat=True)
        count = users.count()
        #users = list(users.keys())
        randomCountries = random.sample(list(countriesToAcr.keys()), count)
        for i in range(0,count,1):
            countryAdd = country(name=randomCountries[i], 
                                 occupier = WormUser.objects.get(id=users[i]),
                                 lobby = Lobby.objects.get(lobbyPK = lobbyID), 
                                 gucci = 100,
                                 food = 100,
                                 occupyingForce=100,
                                 troopGen = 100,
                                 color = 'red')
            countryAdd.save()

class userOccupying(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        countries = country.objects.filter(lobby=body["LobbyID"],occupier=WormUser.objects.get(username=body["Username"].strip()).id).values_list('name', flat=True)
        return JsonResponse({'States':list(countries)})
    

class lobbyChoice(TemplateView):
    template_name = 'selectLobby.html'
    objects = [Lobby]
    keywords = ["Lobbys"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for keyword, object in zip(self.keywords, self.objects):
            context[keyword] = object.objects.all()
        return context

def loginPageLoad(request):

    if request.user.is_authenticated:
        return redirect('lobbies')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lobbies')

            else:
                return render(request, 'login.html', {'form':form})
        else:
            return render(request, 'login.html', {'form':form})
    else:
        return render(request, 'login.html', {'form':AuthenticationForm()})

def newLobby(request):
    user = WormUser.objects.get(id = request.user.id)
    lobby = Lobby(owner=user)
    lobby.save()
    lobby.wormuser.add(user, through_defaults={'color':'Red'})
    return redirect('game', lobby.lobbyPK)

def signout(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('lobbies')

    if request.method == 'POST':
        form = newUserForm(data = request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  
            login(request, user)
            return redirect('lobbies')
        else:
            return render(request, 'register.html', {'form':form})
    else:
        return render(request, 'register.html', {'form':newUserForm()})

def selectColorUser(request, lobbyID, color):
    userInLobby.objects.filter(
        user = request.user.id,
        lobby = lobbyID
    ).update(color=color)
    return HttpResponse("Yellow", content_type="text/plain")

#"sm_state sm_state_(acronym)" this is class tag
def stateUpdate(request, lobbyID, stateID):
    userColor = userInLobby.objects.get(
        user = request.user.id,
        lobby = lobbyID
    ).color
    if not country.objects.filter(name=stateID, lobby=lobbyID):
        count = country(
            name = stateID, 
            occupier = WormUser.objects.get(id=request.user.id),
            color = userColor,
            lobby = Lobby.objects.get(lobbyPK=lobbyID),
            gucci = 100,
            food = 100,
            occupyingForce = 100,
            troopGen = 100
            )
        count.save()
    return JsonResponse({'state':countriesToAcr[stateID],'color':userColor})