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

class Session(models.Model):
    Number = models.PositiveIntegerField()
    Name = models.CharField(max_length=20)
    Start = models.DateTimeField()
    End = models.DateTimeField()
    def __unicode__(self):
        return "%s --- %s to %s" % (self.Name, self.Start, self.End)


class ClassRoom(models.Model):
    Number = models.PositiveIntegerField()
    Medium = models.CharField(max_length=5)
    Name = models.CharField(max_length=30)
    Capacity = models.PositiveIntegerField()
    Session = models.ForeignKey(Session)
    def __unicode__(self):
        return "%s --- %s --- %s" % (self.Name, self.Medium, self.Capacity)



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
    def __unicode__(self):
        return "%s %s" % (self.FirstName, self.LastName)

class HallTicket(models.Model):
    Student = models.ForeignKey(Student)
    ClassRoom = models.ForeignKey(ClassRoom)
    SeatNumber = models.PositiveIntegerField()
    def __unicode__(self):
        return "%s %s %s %s" % (self.Student, self.ClassRoom.Session, self.ClassRoom, self.SeatNumber)


class ApplicationForm(forms.Form):
    FirstName = forms.CharField(max_length=30)
    MiddleName = forms.CharField(max_length=30)
    LastName = forms.CharField(max_length=30)
    FatherName = forms.CharField(max_length=30, required=False)
    MotherName = forms.CharField(max_length=30, required=False)
    Address = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':4}),max_length=30)
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
    
class GenerateHallTicketForm(forms.Form):
    FirstName = forms.CharField(max_length=30)
    LastName = forms.CharField(max_length=30)

class Exam(models.Model):
    Name = models.CharField(max_length=30, primary_key=True)
    Medium = models.CharField(max_length=5)

class QuestionAnswerKey(models.Model):
    Exam = models.ForeignKey(Exam, unique=True)
    Number = models.PositiveIntegerField(unique=True)
    Answer = models.CharField(max_length=10)
    
class ExamResponse(models.Model):
    Student = models.ForeignKey(Student)
    QuestionAnswerKey = models.ForeignKey(QuestionAnswerKey)
    Answer = models.CharField(max_length=10)