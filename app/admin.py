from django.contrib import admin
from .models import Group, Chat, AddFriends
# Register your models here.
@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'timestamp', 'group', 'send_msg_friend', 'receive_msg_friend']


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(AddFriends)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'request_friends', 'receive_friends', 'relationship']