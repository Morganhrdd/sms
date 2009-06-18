from django.db import models
from django import forms
from jp_sms.students.models import StudentBasicInfo, AcademicYear, ClassMaster, StudentYearlyInformation, STANDARD_CHOICES

# Create your models here.

RECEIPT_CHOICES = (
    (1, 'Valid'),
    (2, 'Cancel'),
)

FEE_FILTER_CHOICES = (
	(1, 'All'),
	(2, 'Defaulters')
)

FEE_DIVISION_CHOICES = (
    ('A', 'All'),
    ('G', 'Girls'),
    ('B', 'Boys'),
)

class FeeType(models.Model):
	ClassMaster = models.ForeignKey(ClassMaster)
	Type = models.CharField(max_length=30)
	Amount = models.PositiveIntegerField()
	def __unicode__(self):
		return "%s, %d" % (self.Type, self.Amount)
				
class FeeReceipt(models.Model):
	ReceiptNumber = models.PositiveIntegerField(primary_key=True)
	Date = models.DateField()
	StudentYearlyInformation = models.ForeignKey(StudentYearlyInformation)
	FeeType = models.ForeignKey(FeeType)
	Amount = models.PositiveIntegerField()
	ChequeNo = models.PositiveIntegerField(null=True,blank=True)
	Bank = models.CharField(max_length=30,null=True,blank=True)
	Status = models.PositiveIntegerField(choices=RECEIPT_CHOICES)
	
class FeeForm(forms.Form):
	RegNo = forms.IntegerField()
	Name = forms.CharField(required=False)
	Std = forms.IntegerField(required=False)
	Year = forms.CharField(required=False)
	FeeType = forms.CharField(required=False)
	Amount = forms.IntegerField(required=False)
	ChequeNo = forms.IntegerField(required=False)
	Bank = forms.CharField(required=False)
	
class FeeReportForm(forms.Form):
	Std = forms.IntegerField(required=False)
	Year = forms.CharField(required=True)
	Division = forms.ChoiceField(choices=FEE_DIVISION_CHOICES)
	Show = forms.ChoiceField(choices=FEE_FILTER_CHOICES)

class FeeCollectionForm(forms.Form):
	Date =  forms.DateField(widget=forms.DateTimeInput)
