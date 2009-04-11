# Create your views here.

from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
import os
import datetime
from array import array

from jp_sms.fees.models import StudentBasicInfo, AcademicYear, ClassMaster, StudentYearlyInformation
from jp_sms.fees.models import FeeType, FeeReceipt
from jp_sms.fees.models import FeeForm

def fee_receipt(request):
	message = "";
	dt = datetime.datetime.now()
	date = dt.date()
	receiptnumber = "------"
	if not request.POST:
		form = FeeForm()
		return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber})
	else:
		form = FeeForm(request.POST)
		if not form.is_valid():
			return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber})
		if request.POST['applyforfee'] == '1':
			if form.is_valid():
				regno = form.cleaned_data['RegNo']
				studentbi = StudentBasicInfo.objects.filter(RegistrationNo=regno)
				if not studentbi:
					message = "Invalid Registration Number"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					
				student = studentbi[0]

				year = form.cleaned_data['Year']
				acadyears = AcademicYear.objects.filter(Year=year)
				if not acadyears:
					message = "Enter valid academic year"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					
					
				acadyr = acadyears[0]
				std = form.cleaned_data['Std']
				if not std:
					message = "Enter the Standard"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					

				cms = ClassMaster.objects.filter(AcademicYear=acadyr).filter(Standard=std)
				if not cms:
					message = "Invalid Standard"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					
					
				classmaster = cms[0]
				studentyearlyinfo = StudentYearlyInformation.objects.filter(StudentBasicInfo=student).filter(ClassMaster=classmaster)
				if not studentyearlyinfo:
					message = "Student not enrolled"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					
				
				feetype = form.cleaned_data['FeeType']
				amount = form.cleaned_data['Amount']
				
				if (not feetype):
					message = "Please enter the fee type"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })
				if (not amount):
					message = "Please enter the amount"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })

				ftypes = FeeType.objects.filter(ClassMaster=classmaster).filter(Type=feetype)
				if not ftypes:
					message = "Invalid Fee Type"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })
					
				cheque = form.cleaned_data['ChequeNo']
				bank = form.cleaned_data['Bank']
				if cheque and (not bank):
					message = "Please enter bank details"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })
				if bank and (not cheque):
					message = "Please enter cheque number"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })
					
				fr = FeeReceipt.objects.all().order_by('-ReceiptNumber')
				if fr:
					id = fr[0].ReceiptNumber
					if id <= 100000:
						id = 100001
					else:
						id = id + 1
				else:
					id = 100001
					
				feereceipt = FeeReceipt()
				feereceipt.ReceiptNumber = id
				feereceipt.StudentYearlyInformation = studentyearlyinfo[0]
				feereceipt.Date = date
				feereceipt.FeeType = ftypes[0]
				feereceipt.Amount = amount
				feereceipt.ChequeNo = cheque
				feereceipt.Bank = bank
				feereceipt.Status = 1
				feereceipt.save()
				message = "Fee receipt " + str(feereceipt.ReceiptNumber) + " generated"
				receiptnumber = feereceipt.ReceiptNumber
				print message
				return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					

		elif request.POST['applyforfee'] == '0':
			if form.is_valid():
				regno = form.cleaned_data['RegNo']
				studentbi = StudentBasicInfo.objects.filter(RegistrationNo=regno)
				if not studentbi:
					message = "Invalid Registration Number"
					return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					
				student = studentbi[0]

				years = []
				classmaster = StudentYearlyInformation.objects.filter(StudentBasicInfo=student)
				if classmaster:
					for data in classmaster:
						feetypes = FeeType.objects.filter(ClassMaster=data.ClassMaster)
						feeinfo = []
						if feetypes:
							for ftype in feetypes:
								feereceipts = FeeReceipt.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype).filter(Status=1)
								feedateamount = []
								total = 0
								if feereceipts:
									for fr in feereceipts:
										feedateamount.append({'ReceiptNo':fr.ReceiptNumber, 'Date':fr.Date, 'Amount':fr.Amount})
										total += fr.Amount
								feeinfo.append({'Type':ftype.Type, 'Amount':ftype.Amount, 'FeeDateAmount': feedateamount, 'Total':total,
												 'Balance':ftype.Amount - total})
						years.append({'ClassMaster':data.ClassMaster, 'FeeInfo': feeinfo})															

				return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,
											'receiptnumber':receiptnumber, 'student':student, 'years':years })					
						