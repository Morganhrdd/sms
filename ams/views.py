# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
import os
import datetime

from jp_sms.ams.models import Category, User, UserStatus, TimeRecords, DayRules, TimeRules, Attendance
from jp_sms.ams.models import Leaves, LeaveForm, LeaveRules, AcademicYear
from jp_sms.ams.models import LEAVE_CHOICES

def get_barcode(request):
	message = ""
	if request.GET.has_key('barcode'):
		dt = datetime.datetime.now()
		date = dt.date()
		time = dt.time()
		day = dt.isoweekday()
		
		barcode = request.GET['barcode']
		user = User.objects.filter(Barcode=barcode)[0]
		userstatus = UserStatus.objects.filter(Barcode=barcode)[0]
		category = user.Category
		status = userstatus.Status

		remqs = Attendance.objects.filter(Date=date).filter(Barcode=barcode)
				
		if status == 'I':
			userstatus.Status = 'O'
			if remqs:
				rem = remqs[0].Remark
				lastin = TimeRecords.objects.filter(Date=date).filter(Barcode=barcode).filter(Type='I')[0].Time
				t1_m = lastin.hour*60 + lastin.minute
				t2_m = time.hour*60 + time.minute
				if t2_m - t1_m < 1:
					message = "user already checked in"
					return populate_user(request,message)		
		else:
			if remqs:
				rem = remqs[0].Remark
				lastinrec = TimeRecords.objects.filter(Date=date).filter(Barcode=barcode).filter(Type='O')
				if lastinrec:
					lastin = lastinrec[0].Time
					t1_m = lastin.hour*60 + lastin.minute
					t2_m = time.hour*60 + time.minute
					if t2_m - t1_m < 1:
						message = "user already checked out"
					else:
						message = "user entry for today already marked"
					return populate_user(request,message)		
			userstatus.Status = 'I'

		message = "user time recorded "
		userstatus.save()
		status = userstatus.Status
		
		timerc = TimeRecords()
		timerc.Barcode = user
		timerc.Type = userstatus.Status
		timerc.Date = date
		timerc.Time = time
		timerc.save()
		
		if remqs:
			if (rem == 'O') or (rem == 'C') or (status == 'I'):
				message = "user entry for today already marked"
				return populate_user(request,message)		
			
		dayrule = DayRules.objects.filter(Date=date).filter(Barcode=barcode)
		if not dayrule:
			dayrule = DayRules.objects.filter(Date=date).filter(Category=category)
			if not dayrule:
				dayrule = DayRules.objects.filter(Day=day).filter(Barcode=barcode)
				if not dayrule:
					dayrule = DayRules.objects.filter(Day=day).filter(Category=category)
					
		if dayrule:
			timerule = dayrule[0].Type

			if status == 'I':
				if timerule == TimeRules.objects.filter(Type='Holiday')[0]:
					remark = 'S'
					attendance = Attendance()
					attendance.Barcode = user
					attendance.Date = date
					attendance.Remark = remark
					attendance.Year = AcademicYear.objects.filter(Status=1)[0]
					attendance.save()
					message = "today is a holiday. remember to checkout"
					return populate_user(request,message)		
				
				t1_m = time.hour*60 + time.minute
				t2_m = timerule.HalfIn.hour*60 + timerule.HalfIn.minute
				if t1_m > t2_m + 15:
					remark = 'A'
				elif time > timerule.HalfIn:
					tattendance = TempAttendance()
					tattendance.Barcode = user
					tattendance.Remark = 'L'
					tattendance.save()
					remark = 'H'	
				elif time > timerule.LateIn:
					remark = 'H'
				elif time > timerule.TimeIn:
					remark = 'L'
				else:
					remark = 'P'
				attendance = Attendance()
				attendance.Barcode = user
				attendance.Date = date
				attendance.Remark = remark
				attendance.Year = AcademicYear.objects.filter(Status=1)[0]
				attendance.save()
				
				startdate = attendance.Year.StartDate
				oneday = datetime.timedelta(1)
				while 1:
					date = date - oneday
					day = date.isoweekday()
					existingattendance = Attendance.objects.filter(Date=date).filter(Barcode=barcode)
					if existingattendance:
						if (existingattendance[0].Remark == 'O') or (existingattendance[0].Remark == 'C'):
							continue
						else:
							break
						
					else:
						if date < startdate:
							break

						dayruleh = DayRules.objects.filter(Date=date).filter(Barcode=barcode)
						if not dayruleh:
							dayruleh = DayRules.objects.filter(Date=date).filter(Category=category)
							if not dayruleh:
								dayruleh = DayRules.objects.filter(Day=day).filter(Barcode=barcode)
								if not dayruleh:
									dayruleh = DayRules.objects.filter(Day=day).filter(Category=category)
						if (dayruleh) and (dayruleh[0].Type == TimeRules.objects.filter(Type='Holiday')[0]):
							remark = 'S'
						else:
							remark = 'A'

						attendance = Attendance()
						attendance.Barcode = user
						attendance.Date = date
						attendance.Remark = remark
						attendance.Year = AcademicYear.objects.filter(Status=1)[0]
						attendance.save()
						
			else:
				t1_m = time.hour*60 + time.minute
				t2_m = timerule.HalfOut.hour*60 + timerule.HalfOut.minute
				if rem == 'P':
					if t1_m < t2_m - 15:
						remark = 'A'
					elif time < timerule.HalfOut:
						attendance = Attendance()
						attendance.Barcode = barcode
						attendance.Remark = 'E'
						attendance.Date = date
						attendance.Year = AcademicYear.objects.filter(Status=1)[0]
						attendance.save()
						remark = 'H'
					elif time < timerule.EarlyOut:
						remark = 'H'
					elif time < timerule.TimeOut:
						remark = 'E'
					else:
						remark = 'P'
				elif rem == 'L':
					if t1_m < t2_m - 15:
						remark = 'A'
					elif time >= timerule.TimeOut:
						remark = 'L'
					else:
						attendance = Attendance()
						attendance.Barcode = barcode
						attendance.Remark = rem
						attendance.Date = date
						attendance.Year = AcademicYear.objects.filter(Status=1)[0]
						attendance.save()
						
						if time < timerule.HalfOut:
							attendance = Attendance()
							attendance.Barcode = barcode
							attendance.Remark = 'E'
							attendance.Date = date
							attendance.Year = AcademicYear.objects.filter(Status=1)[0]
							attendance.save()
							remark = 'H'
						elif time < timerule.EarlyOut:
							remark = 'H'
						else:
							remark = 'E'
				elif rem == 'H':
					tattendance = TempAttendance.objects.filter(Barcode=barcode)[0]
					if time < timerule.EarlyOut:
						remark = 'A'
						if tattendance:
							tattendance.delete()
					else:
						if tattendance:
							attendance = Attendance()
							attendance.Barcode = tattendance.Barcode
							attendance.Remark = tattendance.Remark
							attendance.Date = date
							attendance.Year = AcademicYear.objects.filter(Status=1)[0]
							attendance.save()
							tattendance.delete()
						if time < timerule.TimeOut:
							attendance = Attendance()
							attendance.Barcode = barcode
							attendance.Remark = 'E'
							attendance.Date = date
							attendance.Year = AcademicYear.objects.filter(Status=1)[0]
							attendance.save()
						remark = 'H'
				elif rem == 'A':
					remark = 'A'
				else:
					remark = rem
						
				attendance = remqs[0]
				attendance.Remark = remark
				attendance.Year = AcademicYear.objects.filter(Status=1)[0]
				attendance.save()
		else:
			print "No day rule found"
			
	return populate_user(request,message)		
	
def populate_user(request,message):
	usersin = UserStatus.objects.filter(Status='I')
	usersout = UserStatus.objects.filter(Status='O')
	yettocome = []
	gone = []
	absent = []
	come = []
	dt = datetime.datetime.now()
	date = dt.date()
	for usr in usersout:
		attrcd = Attendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
		if attrcd:
			rem = attrcd[0].Remark
			if rem == 'O':
				absent.append({'user': usr})
			else:
				gone.append({'user': usr})
		else:
			yettocome.append({'user': usr})
	for usr in usersin:
		attrcd = Attendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
		if attrcd:
			rem = attrcd[0].Remark
			if rem == 'O':
				absent.append({'user': usr})
			else:
				come.append	({'user': usr})
	return render_to_response('ams/barcode.html',Context({'come': come,'yettocome':yettocome,'gone':gone,'absent':absent,'message':message}))

def app_leave(request):
	message = "";
	if not request.GET:
		form = LeaveForm()
		return render_to_response('ams/leaveapp.html', {'form': form})
	else:
		form = LeaveForm(request.GET)
		if not form.is_valid():
			return render_to_response('ams/leaveapp.html', {'form': form})
		if request.GET['applyforleave'] == '1':
			if form.is_valid():
				ldate = form.cleaned_data['Date']
				barcode = form.cleaned_data['Barcode']
				prevapp = Leaves.objects.filter(LeaveDate=ldate).filter(Barcode=barcode)
				if prevapp:
					message = "Already applied for leave on given date"
				else:
					leaves  = Leaves()
					leaves.LeaveDate = form.cleaned_data['Date']
					if leaves.LeaveDate:
						leaves.ApplicationDate = datetime.datetime.now().date()
						leaves.Type = form.cleaned_data['Type']
						leaves.Status = 1
						leaves.Barcode = form.cleaned_data['Barcode']
						leaves.save()
					else:
						message = "Supply the Date for leave application!"
			
		barcode = form.cleaned_data['Barcode']
		category = form.cleaned_data['Category']
		pendingleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=1)
		approveleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=2)

		data = []
		for type in LEAVE_CHOICES:
			leavetype = type[0]
			total = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)[0].Days
			pending = pendingleaves.filter(Type=leavetype).count()
			approve = approveleaves.filter(Type=leavetype).count()
			data.append({'type':type[1], 'total':total, 'approve': approve, 'pending':pending, 'balance':total-approve-pending })

		adays = Attendance.objects.filter(Barcode=barcode).filter(Remark='A')
		absentdays = adays.count()
		latedays = Attendance.objects.filter(Barcode=barcode).filter(Remark='L').count()
		halfdays = Attendance.objects.filter(Barcode=barcode).filter(Remark='H').count()
		abdays = []
		for day in adays:
			abdays.append({'date':day.Date})
			
		return render_to_response('ams/leaveapp.html', {'form': form, 'data': data, 'message': message, 'abdays': abdays, 'latedays': latedays, 'halfdays': halfdays, 'absentdays': absentdays})
		