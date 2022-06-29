from ipaddress import ip_address
import ipaddress
from urllib import response
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.humanize.templatetags.humanize import naturaltime
# from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from requests import session
from .models import UserProfile, Message
from django.db.models import Q
from django.shortcuts import redirect
import json
#from .forms import UserProfileForm
from faker import Faker
fake = Faker()






def chat_icon(request):
    return render(request,"icon.html")

@csrf_exempt
def homepage(request): 
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')    ### Real IP address of client Machine
    print("------------------------------------------")
    username = fake.first_name()
    user = UserProfile(username=username, ip_address = ip)
    other_user = UserProfile.objects.get(username = "DataBeat")
    if  UserProfile.objects.filter(ip_address = ip).exists():
        if UserProfile.objects.filter(ip_address = ip)[0].username=="DataBeat" or UserProfile.objects.filter(username=username).exists():
            if  UserProfile.objects.filter(ip_address = ip)[0].username=="DataBeat":
                receiver1 = UserProfile.objects.filter(ip_address =ip, username="DataBeat")
            else:
                receiver1 = UserProfile.objects.filter(ip_address =ip, username=username)
            print(receiver1[0])
            if receiver1[0].id != UserProfile.objects.filter(username = "DataBeat")[0].id and other_user == UserProfile.objects.filter(username = "DataBeat")[0]:
                messages = Message.objects.filter(
                    Q(receiver= receiver1[0].id, sender=other_user.id)
                )
                print(messages)
                messages.update(seen=True)
                messages = messages | Message.objects.filter(Q(receiver=other_user.id, sender=receiver1[0].id) )
                # print(messages)
                return render(request, "chatroom1.html", {"other_user": other_user, 'users': UserProfile.objects.filter(username = "DataBeat") ,"receiver": receiver1[0].username ,"user_messages": messages})
        else:
            user.save()
            receiver1 = UserProfile.objects.filter(username= username,ip_address =ip)
            if other_user == UserProfile.objects.filter(username = "DataBeat")[0]:
                messages = Message.objects.filter(
                    Q(receiver= receiver1[0].id, sender=other_user.id)
                )
                print(messages)
                messages.update(seen=True)
                messages = messages | Message.objects.filter(Q(receiver=other_user.id, sender= receiver1[0].id) )
                # print(messages)
                response= render(request, "chatroom1.html", {"other_user": other_user, 'users': UserProfile.objects.filter(username = "DataBeat"), "receiver": receiver1[0].username,"user_messages": messages})
                response.set_cookie('username', receiver1[0].username)
                return response
        
    else:
        user.save()
        receiver1 = UserProfile.objects.filter(username= username,ip_address =ip)
        if other_user == UserProfile.objects.filter(username = "DataBeat")[0]:
            messages = Message.objects.filter(
                Q(receiver= receiver1[0].id, sender=other_user.id)
            )
            print(messages)
            messages.update(seen=True)
            messages = messages | Message.objects.filter(Q(receiver=other_user.id, sender= receiver1[0].id) )
            # print(messages)
            response= render(request, "chatroom1.html", {"other_user": other_user, 'users': UserProfile.objects.filter(username = "DataBeat"), "receiver": receiver1[0].username,"user_messages": messages})
            response.set_cookie('username', receiver1[0].username)
            return response
    receiver1 = UserProfile.objects.filter(ip_address =ip)
    if receiver1[0].id == UserProfile.objects.get(username = "DataBeat").id:
        messages = Message.objects.filter(
            Q(receiver= receiver1[0].id, sender=other_user.id)
        )
        print(messages)
        messages.update(seen=True)
        messages = messages | Message.objects.filter(Q(receiver=other_user.id, sender=receiver1[0].id) )
        print(messages)
        response =  render(request, "chatroom1.html", {"other_user": other_user, 'users': UserProfile.objects.exclude(ip_address=ip), "receiver": receiver1[0].username ,"user_messages": messages})
        response.set_cookie('username', receiver1[0].username)
        return response

    


@csrf_exempt
def chatroom(request, pk:int):
    
    other_user = get_object_or_404(UserProfile, pk=pk)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    if request.COOKIES['username'] != None:
        username=request.COOKIES['username']
        receiver1 = UserProfile.objects.filter(ip_address=ip,username=username)
    # receiver1 = UserProfile.objects.filter(ip_address =ip)
    if other_user == UserProfile.objects.filter(username = "DataBeat")[0]:
        messages = Message.objects.filter(
            Q(receiver= receiver1[0].id, sender=other_user.id)
        )
        messages.update(seen=True)
        messages = messages | Message.objects.filter(Q(receiver=other_user.id, sender=receiver1[0].id) )
        #print(messages)
        return render(request, "chatroom1.html", {"other_user": other_user, 'users': UserProfile.objects.filter(username = "DataBeat"),"receiver": receiver1[0].username, "user_messages": messages})
    else:
        messages = Message.objects.filter(
            Q(receiver= receiver1[0].id, sender=other_user.id)
        )
        #print(messages)
        messages.update(seen=True)
        messages = messages | Message.objects.filter(Q(receiver=other_user.id, sender=receiver1[0].id) )
        return render(request, "chatroom1.html", {"other_user": other_user,'users': UserProfile.objects.exclude(ip_address=ip),"receiver": receiver1[0].username, "user_messages": messages})

@csrf_exempt
def ajax_load_messages(request, pk):
    other_user = get_object_or_404(UserProfile, pk=pk)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if 'username' in request.COOKIES:
        username=request.COOKIES.get('username')
        receiver1 = UserProfile.objects.filter(username=username)
    else:
        receiver1 = UserProfile.objects.filter(ip_address=ip)
    #print(username)
    # print(receiver1[0])
    messages = Message.objects.filter(seen=False, receiver=receiver1[0])
    message_list = [{
        "sender": message.sender.username,
        "receiver":receiver1[0].username,
        "message": message.message,
        "sent": message.sender == receiver1[0].id,
        "date_created": naturaltime(message.date_created),
        

    } for message in messages]
    messages.update(seen=True)
    
    
    if request.method == "POST":
        message = json.loads(request.body)['message']
        m = Message.objects.create(receiver=other_user, sender=receiver1[0] , message=message)
        message_list.append({
            "sender": receiver1[0].username,
            "receiver":other_user.username,
            "username": receiver1[0].username,
            "message": m.message,
            "date_created": naturaltime(m.date_created),
            "sent": True,
        })
    
    for i in message_list:
        print(i)
    return JsonResponse(message_list, safe=False)
    

