from django.shortcuts import render, redirect, HttpResponse
from .forms import newUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Lobby, WormUser

import os

def gameLobby(request, lobbyID):
    
    lobby = Lobby.objects.get(lobbyPK=lobbyID)
    if lobby.wormuser_set.filter(pk = request.user.id).exists():
        return render(request, 'lobby.html', {'LobbyPK':lobbyID, 'Users':lobby.wormuser_set.all()})
    else:
        lobby.wormuser_set.add(WormUser.objects.get(pk = request.user.id))
        return render(request, 'lobby.html')

def lobbyChoose(request):
    return render(request, 'selectLobby.html', {'Lobbys':Lobby.objects.all()})

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
    lobby = Lobby()
    lobby.save()
    user = WormUser.objects.get(id = request.user.id)
    lobby.wormuser_set.add(user)
    return render(request, 'lobby.html', {'Players':lobby})

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

def stateInfo(request, lobbyID, stateID):
    print(lobbyID)
    print(stateID)
    return HttpResponse(request, "You did it!")