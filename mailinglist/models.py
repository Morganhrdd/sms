from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class Person(models.Model):
    Name = models.CharField(max_length=120)
    Address = models.TextField(max_length=500)
    City = models.CharField(max_length=50, blank=True)
    Taluka = models.CharField(max_length=50, blank=True)
    District = models.CharField(max_length=50, blank=True)
    PinCode = models.CharField(max_length=6, blank=True)
    Phone = models.CharField(max_length=20, blank=True)
    
class PersonSearch(forms.Form):
    Name = forms.CharField()
    Address = forms.CharField()
    City = forms.CharField()
    Taluka = forms.CharField()
    PinCode = forms.CharField()
    District = forms.CharField()
    Phone = forms.CharField()

