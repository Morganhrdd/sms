from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms


MEDIUM_CHOICES = (
	('E', 'English'),
	('M', 'Marathi'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

PAYMODE_CHOICES = (
    ('C', 'Cash'),
    ('DD', 'Demand Draft'),
)
# Create your models here.
class DateTimeDetails(models.Model):
    Start = models.DateTimeField()
    End = models.DateTimeField()
    def __unicode__(self):
        return "%s to %s" % (self.Start.strftime('%d/%m/%y %H:%M'), self.End.strftime('%d/%m/%y %H:%M'))

class ClassRoom(models.Model):
    Number = models.PositiveIntegerField()
    Medium = models.CharField(max_length=5)
    Name = models.CharField(max_length=30)
    Capacity = models.PositiveIntegerField()
    def __unicode__(self):
        return "%s --- %s --- %s" % (self.Name, self.Medium, self.Capacity)

class Session(models.Model):
    Number = models.PositiveIntegerField()
    Name = models.CharField(max_length=20)
    DateTimeDetails = models.ForeignKey(DateTimeDetails)
    classrooms = models.ManyToManyField(ClassRoom)
    def __unicode__(self):
        return "%s --- %s" % (self.Name, self.DateTimeDetails)


class Student(models.Model):
    FirstName = models.CharField(max_length=30)
    MiddleName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    FatherName = models.CharField(max_length=30, blank=True)
    MotherName = models.CharField(max_length=30, blank=True)
    Address = models.CharField(max_length=100)
    Pincode = models.PositiveIntegerField(blank=True)
    PhoneHome = models.CharField(max_length=20, blank=True)
    PhoneMobile = models.CharField(max_length=20, blank=True)
    Email = models.EmailField(blank=True)
    Medium = models.CharField(max_length=10, choices=MEDIUM_CHOICES)
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    DateOfBirth = models.DateField()
    CurrentSchool = models.CharField(max_length=50, blank=True)
    CurrentStd = models.PositiveIntegerField(blank=True)
    PayMode = models.CharField(max_length=20, choices=PAYMODE_CHOICES)
    DDNo = models.CharField(max_length=30, blank=True)

class HallTicket(models.Model):
    Student = models.ForeignKey(Student)
    Session = models.ForeignKey(Session)
    ClassRoom = models.ForeignKey(ClassRoom)
    SeatNumber = models.CharField(max_length=30)


class ApplicationForm(forms.Form):
    FirstName = forms.CharField(max_length=30)
    MiddleName = forms.CharField(max_length=30)
    LastName = forms.CharField(max_length=30)
    FatherName = forms.CharField(max_length=30, required=False)
    MotherName = forms.CharField(max_length=30, required=False)
    Address = forms.CharField(max_length=30)
    Pincode = forms.IntegerField(required=False) 
    PhoneHome = forms.IntegerField(required=False) 
    PhoneMobile = forms.IntegerField(required=False)
    Email = forms.EmailField(required=False)
    Medium = forms.ChoiceField(choices=MEDIUM_CHOICES)
    Gender = forms.ChoiceField(choices=GENDER_CHOICES)
    DateOfBirth = forms.DateField()
    CurrentSchool = forms.CharField(max_length=50, required=False)
    CurrentStd = forms.IntegerField(required=False)
    PayMode = forms.ChoiceField(choices=PAYMODE_CHOICES)
    DDNo = forms.CharField(max_length=30, required=False)