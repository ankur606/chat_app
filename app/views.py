from django.shortcuts import render
from .models import Chat, Group, AddFriends
from  django.http import HttpResponse
# Create your views here.
from django.views import View
import random
from django.db.models import Q
def index(request, group_name):
    print("Group Name", group_name)
    if request.user.is_authenticated:
        group = Group.objects.filter(name=group_name).first()
        chats = []
        if group:
            chats = Chat.objects.filter(group=group)
            print(chats)
        else:
            group = Group(name=group_name)
            group.save()
        
        return render(request, 'app/index.html', {'groupname':group_name, 'chats':chats, 'user_id':request.user.id})
    else:
        
        return HttpResponse("Login Please")
        
# Now we will start this project

class FriendList(View):
    def get(self, request):
        print(request.user)
    
        friends_lists = AddFriends.objects.filter(Q(request_friends=request.user.id) | Q(receive_friends=request.user.id))
        print(friends_lists)
        for i in friends_lists:
            print(i.receive_friends)
        return render(request, 'app/friends-lists.html', {'friends':friends_lists})