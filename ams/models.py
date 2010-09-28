from django.db import models
from django import forms

# import variables
from sms.ams.vars import *


# Create your models here.
class AcademicYear(models.Model):
	Id = models.AutoField(primary_key=True)
	Title = models.CharField(max_length=30)
	StartDate = models.DateField()
	EndDate = models.DateField();
	Status = models.PositiveIntegerField(choices=YEAR_CHOICES)
	def __unicode__(self):
		return "%s" % (self.Title)
	
class Category(models.Model):
	Id = models.PositiveIntegerField(primary_key=True)
	Description = models.CharField(max_length=30)
	def __unicode__(self):
		return "%s" % (self.Description)

class User(models.Model):
	Barcode = models.PositiveIntegerField(primary_key=True)
	Category = models.ForeignKey(Category)
	Name = models.CharField(max_length=30)
	Email = models.EmailField(unique=True)
	def __unicode__(self):
		return "%s" % (self.Name)
	def __str__(self):
		return "%s" % (self.Name)

class UserStatus(models.Model):
	Barcode = models.ForeignKey(User)
	Status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class UserJoiningDate(models.Model):
	Barcode = models.ForeignKey(User)
	JoiningDate = models.DateField();
	
class ForgotCheckout(models.Model):
	Barcode = models.ForeignKey(User)
	Date = models.DateField()
	Status = models.PositiveIntegerField(choices=FORGOT_CHECKOUT_CHOICES)

class TimeRules(models.Model):
	Type = models.CharField(max_length=30,primary_key=True)
	TimeIn = models.TimeField()
	LateIn = models.TimeField()
	HalfIn = models.TimeField()
	HalfOut = models.TimeField()
	EarlyOut = models.TimeField()
	TimeOut = models.TimeField()
	def __unicode__(self):
		return "%s" % (self.Type)
		
class DayRules(models.Model):
	Category = models.ForeignKey(Category)
	Barcode = models.PositiveIntegerField(null=True, blank=True)
	Day = models.PositiveIntegerField(choices=DAY_CHOICES, null=True, blank=True)
	Date = models.DateField(null=True, blank=True)
	Type = models.ForeignKey(TimeRules)
	def __unicode__(self):
		return "%s %s %s %s  -  %s" % (self.Category, self.Barcode, self.Day, self.Date, self.Type)

class Attendance(models.Model):
	Barcode = models.ForeignKey(User)
	Date = models.DateField(null=True, blank=True)
	Remark = models.CharField(max_length=1, choices=REMARK_CHOICES)
	Year = models.ForeignKey(AcademicYear)
	Comment = models.CharField(max_length=30, null=True, blank=True)
	
class LeaveAttendance(models.Model):
	Barcode = models.ForeignKey(User)
	Date = models.DateField(null=True, blank=True)
	Remark = models.CharField(max_length=1, choices=REMARK_CHOICES)

class TempAttendance(models.Model):
	Barcode = models.ForeignKey(User)
	Remark = models.CharField(max_length=1, choices=REMARK_CHOICES)

class TimeRecords(models.Model):
	Barcode = models.ForeignKey(User)
	Type = models.CharField(max_length=1, choices=STATUS_CHOICES)
	Date = models.DateField()
	Time = models.TimeField()

class Leaves(models.Model):
	Barcode = models.ForeignKey(User)
	ApplicationDate = models.DateField()
	LeaveDate = models.DateField()
	ApprovalDate = models.DateField(null=True, blank=True)
	Type = models.PositiveIntegerField(choices=LEAVE_CHOICES)
	Status = models.PositiveIntegerField(choices=LEAVESTATUS_CHOICES)
	Reason = models.CharField(max_length=30, null=True, blank=True)
	def __unicode__(self):
		return "%s %s %s" % (self.Barcode, self.LeaveDate, self.Status)

class LeavesBalance(models.Model):
	Barcode = models.ForeignKey(User)
	Type = models.PositiveIntegerField(choices=LEAVE_CHOICES)
	Days = models.FloatField()

class LeaveRules(models.Model):
	Category = models.ForeignKey(Category)
	Type = models.PositiveIntegerField(choices=LEAVE_CHOICES)
	Days = models.PositiveIntegerField()

class EncashLeaves(models.Model):
	Barcode = models.ForeignKey(User)
	Days = models.PositiveIntegerField()
	Status = models.PositiveIntegerField(choices=LEAVESTATUS_CHOICES)
	
class Overtime(models.Model):
	Barcode = models.ForeignKey(User)
	Date = models.DateField()
	ApprovalDate = models.DateField(null=True, blank=True)
	Hours = models.FloatField()
	Status = models.PositiveIntegerField(choices=LEAVESTATUS_CHOICES)

class LeaveForm(forms.Form):
	Category = forms.ModelChoiceField(queryset=Category.objects.all())
	Barcode = forms.ModelChoiceField(queryset=User.objects.all())
	FromDate =  forms.DateField(widget=forms.DateTimeInput, required=False)
	ToDate =  forms.DateField(widget=forms.DateTimeInput, required=False)
	Days = forms.IntegerField(required=False)
	Type = forms.ChoiceField(choices=LEAVE_CHOICES)
	Reason = forms.CharField(max_length=30, required=False)

class ReportForm(forms.Form):
	Category = forms.ModelChoiceField(queryset=Category.objects.all())
	Barcode = forms.ModelChoiceField(queryset=User.objects.all())
	FromDate =  forms.DateField(widget=forms.DateTimeInput)
	ToDate =  forms.DateField(widget=forms.DateTimeInput)

class DailyReportForm(forms.Form):
	Category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
	Date =  forms.DateField(widget=forms.DateTimeInput)

class DayRulesForm(forms.Form):
	FromDate =  forms.DateField(widget=forms.DateTimeInput)
	ToDate =  forms.DateField(widget=forms.DateTimeInput)
	Category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
	Barcode = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
	Type = forms.ModelChoiceField(queryset=TimeRules.objects.all(), required=False)

class LeaveReportForm(forms.Form):
	Category = forms.ModelChoiceField(queryset=Category.objects.all())
	Barcode = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
	
