from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from django.forms import ModelForm


from django import forms

from django.forms.widgets import CheckboxSelectMultiple, Select

class User(AbstractUser):
    nickname = models.CharField(max_length=254, blank=True)
    #user = models.OneToOneField(User)
    class Meta(AbstractUser.Meta):
        pass
 
    def __str__(self):
        return self.username
    
    def isOwnerOf(self):
        return Event.objects.has_owner(self)
    
    def isVendorOf(self):
        return Event.objects.has_vendor(self)
    
    def isGuestOf(self):
        return Event.objects.has_guest(self)
    
    def createEvent(self, eventName, dateTime):
        newEvent = Event.objects.create_event(eventName, dateTime)
        newEvent.save()
        newEvent.addOwner(self)

class EventManager(models.Manager):
    def create_event(self, eventName, dateTime):
        event = self.create(eventname = eventName, date_time = dateTime)
        return event
    # TO-DO : Can rewrite in terms of SQL queries instead of .all() for optimization
    def has_owner(self, user):
        return [e for e in self.all() if user in e.owners.all()]
    def has_vendor(self, user):
        return [e for e in self.all() if user in e.vendors.all()]
    def has_guest(self, user):
        return [e for e in self.all() if user in e.guests.all()]

class Event(models.Model):
    event_name = models.CharField(max_length = 100)
    event_detail = models.CharField(max_length = 254)
    date_time = models.DateTimeField(default = timezone.now, blank = False)
    owners = models.ManyToManyField(User, related_name = "owners")
    vendors = models.ManyToManyField(User, related_name="vendors")
    guests = models.ManyToManyField(User, related_name="guests")
    objects = EventManager()

    #allow_plus_one = models.BooleanField(default = False)
    #plus_one =models.ManyToManyField(User, related_name = "plus_ones")
    
    def __str__(self):
        return self.event_name
    
    def addOwner(self, user):
        self.owners.add(user)
        
    def addVendor(self, user):
        self.vendors.add(user)
        
    def addGuest(self, user):
        self.guests.add(user)
        
    def getOwners(self):
        return self.owners.all()
    
    def getVendors(self):
        return self.vendors.all()
    
    def getGuests(self):
        return self.guests.all()

    def addUsers(self, newUsers):
        [self.addOwner(new_owner) for new_owner in new_users['new_owners']]
        [self.addVendor(new_vendor) for new_vendor in new_users['new_vendors']]
        [self.addGuest(new_guest) for new_guest in new_users['new_guests']]



    
# Create your models here.
