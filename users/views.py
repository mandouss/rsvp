from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Event,User, Question,Choice
from django.db.models import DateTimeField
from django.forms import modelform_factory
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

from django.core.mail import send_mail
from django.conf import settings

from .forms import RegisterForm, Eventform, QuestionForm, ChoiceForm

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

def reset_password(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = PasswordResetForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            
        if redirect_to:
            return redirect('reset_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordResetForm(request.user)
    return render(request, 'registration/password_reset_form.html', {'form': form, 'next': redirect_to})


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
            event_guests = new_event.getGuests()
            guest_email=[]
            subject = "Attention: New Invitation has come"
            from_email = settings.EMAIL_HOST_USER
            message = "Hi, there. You have been invited in " + new_event.event_name + ". Please RSVP."
            for guest in event_guests:
                guest_email.append(guest.email)
                send_mail(subject, message, from_email, guest_email, fail_silently=False)
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('create_success')
    else:
        new_event_form = Eventform()
    return render(request,'RSVP_WEB/create_event.html',{'form':new_event_form, 'next': redirect_to})


def create_success(request):
    return render(request,'RSVP_WEB/create_success.html')

def manage_event(request): #Owner event
    find_user_result = User.objects.filter(username = request.user.username)
    find_user = find_user_result.first()
    find_user_own_event = find_user.isOwnerOf()
    if_user_own_events = len(find_user_own_event) > 0
    context = {'user':find_user,'owned_event':find_user_own_event,'has_event':if_user_own_events}
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
    context = {'event':event,'event_name':eventname, 'event_date':eventdate,'event_detail':eventdetail,'event_owner':event_owners,'event_vendor':event_vendors,'event_guest':event_guests,'has_vendor':has_vendors,'has_guest':has_guests}
    return render(request, 'RSVP_WEB/event_details.html', context)


def view_questions(request,eventname):
    if not (user_owns_event(request, eventname) or user_vendor_for_event(request, eventname) or user_guest_for_event(request, eventname)):
        return HttpResponse(content="Unauthorized Request!", status=401, reason="Unauthorized")
    else:
        event = Event.objects.filter(pk=eventname).first()
        eventname = event.event_name
        questions = event.question_set.all()
        has_questions = len(questions)
        questions_choices = []
        for index in range(len(questions)):
            questions_choices.append((questions[index],[choice.choice_text for choice in questions[index].choice_set.all()]))
        context = {'event_name':eventname,'event':event,'questions':questions_choices,'has_questions':has_questions}
        return render(request,'RSVP_WEB/view_questions.html',context)
    
    
def add_questions(request,eventname):
    if user_owns_event(request, eventname):
        event = Event.objects.filter(pk=eventname).first()
        if request.method == "POST":
            new_question_form = QuestionForm(request.POST)
            if new_question_form.is_valid():
                new_question = new_question_form.save(commit=False)
                new_question.for_event = event
                new_question.save()
                new_question_form.save_m2m()
                return redirect('view_questions',eventname = event.pk)
            else:
                return redirect('add_questions',eventname = event.pk)
        else:
            curr_question = event.question_set.all()
            has_question = len(curr_question)>0
            #QuestionFactory = modelform_factory(Question,fields = ("text") )
            #new_question_form = QuestionFactory()
            new_question_form = QuestionForm()
            event_name = event.event_name
            context = {'curr_question':curr_question,'has_question':has_question,'event_name':event_name,'event':event,'questionform':new_question_form}
            return render(request,'RSVP_WEB/add_questions.html',context)

def user_owns_event(request, event_pk):
    eventSet = Event.objects.filter(pk = event_pk)
    if len(eventSet) == 0:
        raise Http404("Event does not exist")
    event = eventSet[0]
    user = User.objects.filter(username=request.user.username)[0]
    return event in user.owners.all()


def user_vendor_for_event(request, event_pk):
    eventSet = Event.objects.filter(pk = event_pk)
    if len(eventSet) == 0:
        raise Http404("Event does not exist")
    event = eventSet[0]
    user = User.objects.filter(username=request.user.username)[0]
    return event in user.vendors.all()


def user_guest_for_event(request, event_pk):
    eventSet = Event.objects.filter(pk=event_pk)
    if len(eventSet) == 0:
        raise Http404("Event does not exist")
    event = eventSet[0]
    user = User.objects.filter(username=request.user.username)[0]
    return event in user.guests.all()

def vendor(request):
    find_vendor_result = User.objects.filter(username = request.user.username)
    find_vendor = find_vendor_result[0]
    find_vendor_own_event = find_vendor.isVendorOf()
    if_vendor_own_events = len(find_vendor_own_event) > 0
    context = {'user':find_vendor,'vendor_event':find_vendor_own_event,'has_vendor_event':if_vendor_own_events}
    return render(request,"RSVP_WEB/vendor.html",context)

def guest(request):
    find_guest_result = User.objects.filter(username = request.user.username)
    find_guest = find_guest_result.first()
    find_guest_own_event = find_guest.isGuestOf()
    if_guest_own_events = len(find_guest_own_event) > 0
    context = {'user':find_guest,'guest_event':find_guest_own_event,'has_guest_event':if_guest_own_events}
    return render(request,"RSVP_WEB/guest.html",context)
    
# Create your views here.
