from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Event,User
from django.db.models import DateTimeField

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

from .forms import RegisterForm, Eventform

def home(request):
    #owned_events = foundUser.isOwnerOf()
    #vendor_events = foundUser.isVendorOf()
    #guest_events = foundUser.isGuestOf()
    return render(request, 'home.html')

def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})

def change_password(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')

            if redirect_to:
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {'form': form, 'next': redirect_to})

#user home page below:

def owner(request):
    return render(request, 'RSVP_WEB/owner.html')

def create_event(request):
    username = request.user.username
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == "POST":
        new_event_form = Eventform(request.POST)
        if new_event_form.is_valid():
            print("valid event")
            new_event = new_event_form.save()
            creator = User.objects.filter(username = username)[0]
            new_event.addOwner(creator)
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('create_success')
                messages.error(request,"Invalid, please check date format.")
    else:
        new_event_form = Eventform()
        return render(request,'RSVP_WEB/create_event.html', {'username': username, 'form':new_event_form, 'next': redirect_to})            

def create_success(request):
    return render(request,'RSVP_WEB/create_success.html')

def manage_event(request): #Owner event
    find_user_result = User.objects.filter(username = request.user.username)
    find_user = find_user_result.first()
    find_user_own_event = find_user.isOwnerOf()
    if_user_own_events = len(find_user_own_event) > 0
    context = {'user':find_user,'owned_event':find_user_own_event,'has_event':if_user_own_events}
    return render(request,"RSVP_WEB/view_own_event.html",context)

def vendor_event(request): #Vendor event
    find_vendor_result = User.objects.filter(username = request.user.username)
    find_vendor = find_vendor_result.first()
    find_vendor_own_event = find_vendor.isVendorOf()
    if_vendor_own_events = len(find_vendor_own_event) > 0
    context = {'vendor':find_vendor,'vendor_event':find_vendor_own_event,'has_vendor_event':if_vendor_own_events}
    return render(request,"RSVP_WEB/view_own_event.html",context)

def guest_event(requese):
    find_guest_result = User.objects.filter(username = request.user.username)
    find_guest = find_guest_result.first()
    find_guest_own_event = find_guest.isGuestOf()
    if_guest_own_events = len(find_guest_own_event) > 0
    context = {'guest':find_guest,'guest_event':find_guest_own_event,'has_guest_event':if_guest_own_events}
    return render(request,"RSVP_WEB/view_own_event.html",context)

def overview_event(request,eventname):
    event = Event.objects.filter(pk=eventname)[0]
    eventname = event.event_name
    eventdetail = event.event_detail
    eventdate = event.date_time
    event_owners = event.getOwners()
    event_vendors = event.getVendors()
    event_guests = event.getGuests()
    has_vendors = len(event_vendors) > 0
    has_guests = len(event_guests) > 0
    context = {'event_name':eventname, 'event_date':eventdate,'event_detail':eventdetail,'event_owner':event_owners,'event_vendor':event_vendors,'event_guest':event_guests,'has_vendor':has_vendors,'has_guest':has_guests}
    return render(request, 'RSVP_WEB/event_details.html', context)

def add_guest(request, username):
    user_query_result = User.objects.filter(username=username)
    if len(user_query_result) ==0:
        found_user = User(username = username, email = request.user.email)
        found_user.save()
    else:
        found_user = user_query_result[0]
    owned_events = found_user.isOwnerOf()
    vendor_events = found_user.isVendorOf()
    guest_events = found_user.isGuestOf()
    owns_events = len(owned_events) >0
    has_vendor_events = len(vendor_events) > 0
    has_guest_events = len(guest_events) > 0
    noun = "You" if request.user.username == username else username
    context = {'user' : found_user, 'owned_events' : owned_events, 'owns_events': owns_events, 'vendor_events': vendor_events, 'guest_events': guest_events, 'has_vendor_events' : has_vendor_events, 'has_guest_events' : has_guest_events, 'noun':noun}
    return render(request, 'RSVP_WEB/owner.html', context)


def vendor(request):
    return render(request, 'RSVP_WEB/vendor.html')

def guest(request):
    return render(request, 'RSVP_WEB/guest.html')
    
# Create your views here.

