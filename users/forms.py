#users/forms.py

from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Event
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple, Select

from django.utils import timezone
import datetime

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

        
class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.username     

        
class Eventform(ModelForm):
    event_name = models.CharField(max_length = 100, help_text = "please choose a attractive event name")
    event_detail = forms.CharField(widget=forms.Textarea)
    #start_time = models.TimeField(help_text = "Start Time", input_formats = ['%I:%M %p'])
    event_date = forms.fields.DateTimeField()
    #end_time = models.TimeField(help_text = "End Time", input_formats = ['%I:%M %p'])
    owners = MyModelMultipleChoiceField(queryset = User.objects.all(), widget = CheckboxSelectMultiple(), required = False)
    vendors = MyModelMultipleChoiceField(queryset = User.objects.all(), widget = CheckboxSelectMultiple(), required = False)
    guests = MyModelMultipleChoiceField(queryset = User.objects.all(), widget = CheckboxSelectMultiple(), required = False)
    class Meta:
        model = Event
        fields = ('event_name','event_detail','event_date')

