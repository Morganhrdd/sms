# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
import os
import datetime
from array import array

from jp_sms.ams.models import Category, User, UserStatus, TimeRecords, DayRules, TimeRules, Attendance, TempAttendance, ForgotCheckout
from jp_sms.ams.models import Leaves, LeaveForm, LeaveRules, AcademicYear, LeaveAttendance, LeavesBalance, EncashLeaves, Overtime
from jp_sms.ams.models import UserJoiningDate
from jp_sms.ams.models import LEAVE_CHOICES, REMARK_CHOICES

def get_barcode(request):
	message = ""
	if request.POST.has_key('barcode') and request.POST['barcode'].isdigit():
		dt = datetime.datetime.now()
		date = dt.date()
		time = dt.time()
		day = dt.isoweekday()
		
		barcode = request.POST['barcode']
		userqs = User.objects.filter(Barcode=barcode)
		if not userqs:
			message = "Invalid barcode! Please rescan the barcode"
			return populate_user(request,message)		
		user = userqs[0]
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
					message = str(user) + " already checked in"
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
						message = str(user) + " already checked out"
					else:
						message = str(user) + " entry for today already marked"
					return populate_user(request,message)		
			userstatus.Status = 'I'

		message = "Time " + dt.strftime("%H:%M:%S") + " recorded for " + str(user)
		userstatus.save()
		status = userstatus.Status
		
		timerc = TimeRecords()
		timerc.Barcode = user
		timerc.Type = userstatus.Status
		timerc.Date = date
		timerc.Time = time
		timerc.save()
		
#		if remqs:
#			if (rem == 'O') or (rem == 'C') or (rem == 'D') or (status == 'I'):
#				message = "user entry for today already marked"
#				return populate_user(request,message)		
			
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
				if timerule.Type == 'Holiday':
					remark = 'S'
					attendance = Attendance()
					attendance.Barcode = user
					attendance.Date = date
					attendance.Remark = remark
					attendance.Year = AcademicYear.objects.filter(Status=1)[0]
					attendance.save()
					message = "Today is a holiday. Remember to checkout"
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
					t2_m = timerule.TimeIn.hour*60 + timerule.TimeIn.minute
					if t2_m > t1_m + 60:
						overtime = Overtime()
						overtime.Barcode = user
						overtime.Date = date
						overtime.Hours = (float(t2_m - t1_m)) / 60
						overtime.Status = 1
						overtime.save()
						
				attendance = Attendance()
				attendance.Barcode = user
				attendance.Date = date
				attendance.Remark = remark
				attendance.Year = AcademicYear.objects.filter(Status=1)[0]
				attendance.save()
				
				startdate = attendance.Year.StartDate
				userjoindate = UserJoiningDate.objects.filter(Barcode=barcode)
				if userjoindate:
					if startdate < userjoindate[0].JoiningDate:
						startdate = userjoindate[0].JoiningDate
				oneday = datetime.timedelta(1)
				while 1:
					date = date - oneday
					day = date.isoweekday()
					existingattendance = Attendance.objects.filter(Date=date).filter(Barcode=barcode)
					if existingattendance:
						leaveattendance = LeaveAttendance.objects.filter(Date=date).filter(Barcode=barcode)
						if leaveattendance:
							if leaveattendance[0].Remark == 'F':
								pendingdeny = 1
								for atten in existingattendance:
									if atten.Remark == 'H':
										atten.Remark = 'F'
										atten.save()
										pendingdeny = 0
										break
								if pendingdeny:
									leaveapp = Leaves.objects.filter(LeaveDate=date).filter(Barcode=barcode)[0]
									leaveapp.Status = 4
									leaveapp.save()
							else:
								if existingattendance[0].Remark == 'A':
									existingattendance[0].Remark = leaveattendance[0].Remark
									existingattendance[0].save()
								else:
									leaveapp = Leaves.objects.filter(LeaveDate=date).filter(Barcode=barcode)[0]
									leaveapp.Status = 4
									leaveapp.save()
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
						if (dayruleh) and (dayruleh[0].Type.Type == 'Holiday'):
							premark = 'S'
						else:
							leaveattendance = LeaveAttendance.objects.filter(Date=date).filter(Barcode=barcode)
							if leaveattendance:
								if leaveattendance[0].Remark == 'F':
									premark = 'A'
								else:
									premark = leaveattendance[0].Remark
							else:
								premark = 'A'

						attendance = Attendance()
						attendance.Barcode = user
						attendance.Date = date
						attendance.Remark = premark
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
						
				t2_m = timerule.TimeOut.hour*60 + timerule.TimeOut.minute
				if t1_m > t2_m + 60:
					overtime = Overtime()
					overtime.Barcode = user
					overtime.Date = date
					overtime.Hours = (float(t1_m - t2_m)) / 60
					overtime.Status = 1
					overtime.save()

				attendance = remqs[0]
				attendance.Remark = remark
				attendance.Year = AcademicYear.objects.filter(Status=1)[0]
				attendance.save()
			for tmprem in REMARK_CHOICES:
				if remark == tmprem[0]:
					message = message + " as " + tmprem[1]
 
		else:
			print "No day rule found"
			
	return populate_user(request,message)		
	
def populate_user(request,message):
	datet = datetime.datetime.now()
	jsdate = datet.strftime("%Y,%m,%d,%H,%M,%S")
	datestr = datet.strftime("%A, %B %d, %Y")
	usersin = UserStatus.objects.filter(Status='I')
	usersout = UserStatus.objects.filter(Status='O')
	forgotcheckout = []
	yettocome = []
	gone = []
	absent = []
	come = []
	dt = datetime.datetime.now()
	date = dt.date()

	for usr in usersout:
		attrcd = Attendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
		if attrcd:
			gone.append({'user': usr})
			rem = attrcd[0].Remark
			if rem == 'O':
				absent.append({'user': usr, 'remark': 'OnLeave'})
			elif rem == 'D':
				absent.append({'user': usr, 'remark': 'OnDuty'})
			elif rem == 'C':
				absent.append({'user': usr, 'remark': 'Compensatory Off'})
			if rem == 'F':
				leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
				if leaves:
					lchoice = leaves[0].Type
					if lchoice == 5:
						absent.append({'user': usr, 'remark': 'First Half'})
					elif lchoice == 6:
						absent.append({'user': usr, 'remark': 'Second Half'})
		lattrcd = LeaveAttendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
		if lattrcd:
			rem = lattrcd[0].Remark
			if rem == 'O':
				absent.append({'user': usr, 'remark': 'OnLeave'})
			elif rem == 'D':
				absent.append({'user': usr, 'remark': 'OnDuty'})
			elif rem == 'C':
				absent.append({'user': usr, 'remark': 'Compensatory Off'})
			if rem == 'F':
				leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
				if leaves:
					lchoice = leaves[0].Type
					if lchoice == 5:
						absent.append({'user': usr, 'remark': 'First Half'})
					elif lchoice == 6:
						absent.append({'user': usr, 'remark': 'Second Half'})
		if not attrcd and not lattrcd:
			yettocome.append({'user': usr})

	for usr in usersin:
		attrcd = Attendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
		if attrcd:
			come.append	({'user': usr})
			rem = attrcd[0].Remark
			if rem == 'O':
				absent.append({'user': usr, 'remark': 'OnLeave'})
			elif rem == 'D':
				absent.append({'user': usr, 'remark': 'OnDuty'})
			elif rem == 'C':
				absent.append({'user': usr, 'remark': 'Compensatory Off'})
			if rem == 'F':
				leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
				if leaves:
					lchoice = leaves[0].Type
					if lchoice == 5:
						absent.append({'user': usr, 'remark': 'First Half'})
					elif lchoice == 6:
						absent.append({'user': usr, 'remark': 'Second Half'})
		lattrcd = LeaveAttendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
		if lattrcd:
			rem = lattrcd[0].Remark
			if rem == 'O':
				absent.append({'user': usr, 'remark': 'OnLeave'})
			elif rem == 'D':
				absent.append({'user': usr, 'remark': 'OnDuty'})
			elif rem == 'C':
				absent.append({'user': usr, 'remark': 'Compensatory Off'})
			if rem == 'F':
				leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
				if leaves:
					lchoice = leaves[0].Type
					if lchoice == 5:
						absent.append({'user': usr, 'remark': 'First Half'})
					elif lchoice == 6:
						absent.append({'user': usr, 'remark': 'Second Half'})
		if not attrcd and not lattrcd:
			usr.Status = 'O'
			usr.save()
			yettocome.append({'user': usr})
			forgot = ForgotCheckout()
			forgot.Barcode = usr.Barcode
			forgot.Status = 1
			
			dat = datet.date()
			oneday = datetime.timedelta(1)
			while 1:
				dat = dat - oneday
				usertr = TimeRecords.objects.filter(Date=dat).filter(Barcode=usr.Barcode).filter(Type='I')
				if usertr:
					forgot.Date = dat
					break
			forgot.save()
	
	usersforgot = ForgotCheckout.objects.filter(Status=1)		
	for usr in usersforgot:
		forgotcheckout.append({'user': usr})

	return render_to_response('ams/barcode.html',Context({'come': come,'yettocome':yettocome,'gone':gone,'absent':absent,
								'forgotcheckout':forgotcheckout,'message':message,'jsdate': jsdate,'datestr': datestr}))

def app_leave(request):
	message = "";
	if not request.POST:
		form = LeaveForm()
		return render_to_response('ams/leaveapp.html', {'form': form})
	else:
		form = LeaveForm(request.POST)
		if not form.is_valid():
			return render_to_response('ams/leaveapp.html', {'form': form})
		if request.POST['applyforleave'] == '1':
			if form.is_valid():
				fdate = form.cleaned_data['FromDate']
				tdate = form.cleaned_data['ToDate']
				barcode = form.cleaned_data['Barcode']
				category = form.cleaned_data['Category']
				reason = form.cleaned_data['Reason']
				
				if (not fdate) or (not tdate):
					message = "Please supply both the dates for leave application"
					return render_to_response('ams/leaveapp.html', {'form': form, 'message': message})
				if fdate <= tdate:
					date = fdate 
					oneday = datetime.timedelta(1)
					while 1:
						day = date.isoweekday()
						dayruleh = DayRules.objects.filter(Date=date).filter(Barcode=barcode.Barcode)
						if not dayruleh:
							dayruleh = DayRules.objects.filter(Date=date).filter(Category=category)
							if not dayruleh:
								dayruleh = DayRules.objects.filter(Day=day).filter(Barcode=barcode.Barcode)
								if not dayruleh:
									dayruleh = DayRules.objects.filter(Day=day).filter(Category=category)
						if (dayruleh) and (dayruleh[0].Type.Type == 'Holiday'):
							pass
						else:
							prevapp = Leaves.objects.filter(LeaveDate=date).filter(Barcode=barcode)
							if prevapp:
								leaves = prevapp[0]
								if leaves.Status == 2:
									if date < datetime.datetime.now().date():
										message = "Leave already approved!"
										return render_to_response('ams/leaveapp.html', {'form': form, 'message': message})
									att = LeaveAttendance.objects.filter(Date=date).filter(Barcode=barcode)
									att[0].delete()
								leaves.Status = 1
								leaves.ApplicationDate = datetime.datetime.now().date()
								leaves.Type = form.cleaned_data['Type']
								leaves.Reason = reason
								leaves.save()
							else:
								leaves  = Leaves()
								leaves.LeaveDate = date
								leaves.ApplicationDate = datetime.datetime.now().date()
								leaves.Type = form.cleaned_data['Type']
								leaves.Status = 1
								leaves.Barcode = form.cleaned_data['Barcode']
								leaves.Reason = reason
								leaves.save()
						
						date = date + oneday
						if date > tdate:
							break
				else:
					message = "Enter correct dates!"
					return render_to_response('ams/leaveapp.html', {'form': form, 'message': message})
				message = "Leave application submitted for user " + str(barcode)
		elif request.POST['applyforleave'] == '2':
			if form.is_valid():
				fdate = form.cleaned_data['FromDate']
				tdate = form.cleaned_data['ToDate']
				barcode = form.cleaned_data['Barcode']
				category = form.cleaned_data['Category']
				if (not fdate) or (not tdate):
					message = "Please supply both the dates for leave cancellation"
					return render_to_response('ams/leaveapp.html', {'form': form, 'message': message})
				if fdate <= tdate:
					date = fdate 
					oneday = datetime.timedelta(1)
					today = datetime.datetime.now().date()
					while 1:
						day = date.isoweekday()

						prevapp = Leaves.objects.filter(LeaveDate=date).filter(Barcode=barcode)
						if prevapp:
							leaves = prevapp[0]
							if (leaves.Status == 2) and (date < today):
								pass
							else:
								if (leaves.Status == 2):
									latten = LeaveAttendance.objects.filter(Date=date).filter(Barcode=barcode)[0]
									latten.delete()
								leaves.delete()
						else:
							if date >= today:	
								latten = LeaveAttendance.objects.filter(Date=date).filter(Barcode=barcode)[0]
								if latten:
									latten[0].delete()

						date = date + oneday
						if date > tdate:
							break
				else:
					message = "Enter correct dates!"
					return render_to_response('ams/leaveapp.html', {'form': form, 'message': message})
				message = "Leave cancellation submitted for user " + str(barcode)
		elif request.POST['applyforleave'] == '3':
			if form.is_valid():
				days = form.cleaned_data['Days']			
				barcode = form.cleaned_data['Barcode']
				category = form.cleaned_data['Category']
				if not days:
					message = "Please give no. of days for encashment!"				
					return render_to_response('ams/leaveapp.html', {'form': form, 'message': message})
				enleave = EncashLeaves()
				enleave.Barcode = barcode
				enleave.Days = days
				enleave.Status = 1
				enleave.save()
				message = "Leave encashment submitted for user " + str(barcode)
				
		barcode = form.cleaned_data['Barcode']
		category = form.cleaned_data['Category']
		pendingleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=1)
		approveleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=2)

		data = []
		balance = [0,0,0,0,0,0,0,0]
		for type in LEAVE_CHOICES:
			leavetype = type[0]
			lrule = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)
			if lrule:
				total = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)[0].Days
			else:
				total = 0
			lvbalance = LeavesBalance.objects.filter(Barcode=barcode).filter(Type=leavetype)
			if lvbalance:
				total += lvbalance[0].Days
				
			pending = pendingleaves.filter(Type=leavetype).count()
			approve = approveleaves.filter(Type=leavetype).count()
			balance[leavetype] = total - approve - pending
			data.append({'type':type[1], 'total':total, 'approve': approve, 'pending':pending, 'balance':total - approve - pending })

		approveenleaves = EncashLeaves.objects.filter(Barcode=barcode).filter(Status=2)
		pendingenleaves = EncashLeaves.objects.filter(Barcode=barcode).filter(Status=1)
		approve = 0
		pending = 0
		for enleave in approveenleaves:
			approve += enleave.Days
		for enleave in pendingenleaves:
			pending += enleave.Days
		data.append({'type':'Encashed', 'total':0, 'approve': approve, 'pending':pending, 'balance':0 })
		
		datedata = []
		for type in LEAVE_CHOICES:
			pendingdates = []
			approvedates = []
			leavetype = type[0]
			pleaves = pendingleaves.filter(Type=leavetype)
			for leave in pleaves:
				print type[1]
				print leave.LeaveDate
				pendingdates.append(leave.LeaveDate)
			aleaves = approveleaves.filter(Type=leavetype)
			for leave in aleaves:
				approvedates.append(leave.LeaveDate)
			datedata.append({'type':type[1], 'approve': approvedates, 'pending':pendingdates})
		print datedata
			
		adays = Attendance.objects.filter(Barcode=barcode).filter(Remark='A')
		latedays = Attendance.objects.filter(Barcode=barcode).filter(Remark='L').count()
		hdays = Attendance.objects.filter(Barcode=barcode).filter(Remark='H')
		abdays = []
		hfdays = []
		absentdays = 0
		halfdays = 0
		for day in adays:
			if not Leaves.objects.filter(Barcode=barcode).filter(LeaveDate=day.Date).filter(Type__in=(1,2,3)):
				abdays.append({'date':day.Date})
				absentdays += 1
		for day in hdays:
			if not Leaves.objects.filter(Barcode=barcode).filter(LeaveDate=day.Date).filter(Type__in=(5,6)):
				hfdays.append({'date':day.Date})
				halfdays += 1
			
		
		total_subtract = (((latedays / 3.0) + halfdays + (-balance[5]) + (-balance[6])) / 2.0)  + absentdays
		if total_subtract > balance[1]:
			total_subtract -= balance[1]
			balance[1] = 0
			balance[3] -= total_subtract
		else:
			balance[1] -= total_subtract

		return render_to_response('ams/leaveapp.html', {'datedata':datedata,'form': form, 'data': data, 'message': message, 'abdays': abdays,
									 'absentdays': absentdays, 'latedays': latedays, 'hfdays':hfdays, 'halfdays': halfdays, 'balance': balance})

def admin_home(request):
	user = request.user
	if user.is_superuser:
		print "superuser"
	else:
		print "not superuser"
