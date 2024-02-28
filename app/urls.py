from django.urls import path
from . import views

urlpatterns = [
    path('<str:group_name>/', views.index, name="ChatPage"),
    path('', views.FriendList.as_view(), name="FriendLists" ),
    
]
