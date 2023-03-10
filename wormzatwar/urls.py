"""wormzatwar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginPageLoad, name="login"),
    path('register/', views.signup, name="register"),
    path('selection/', views.lobbyChoice.as_view(), name="lobbies"),
    path('signout/', views.signout, name='signout'),
    path('newlobby/', views.newLobby, name='newLobby'),
    path('get-occupiers', views.userOccupying.as_view()),
    path('game/<str:lobbyID>', views.gameLobby, name="game"),
    path('game/<str:lobbyID>/startGame', views.startGame.as_view(), name='startGame'),
    path('game/<str:lobbyID>/status', views.gameStatus.as_view(), name='status'),
    path('game/<str:lobbyID>/<str:stateID>', views.stateUpdate, name='state'),
    path('game/<str:lobbyID>/color/<str:color>', views.selectColorUser, name='color'),
]