# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

import os
import datetime

from sms.ams.models import *
from django.contrib.auth.decorators import login_required

# import variables
from sms.ams.vars import *

# import forms
from sms.ams.forms import *

catqs = Category.objects.filter(Description='ALL')
if catqs:
    CATEGORY_ALL = catqs[0]

#
@csrf_exempt
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
            return populate_user(request,message,'ams/barcode.html')        
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
                if t2_m - t1_m < 30:
                    message = str(user) + " already checked in"
                    return populate_user(request,message,'ams/barcode.html')        
        else:
            if remqs:
                rem = remqs[0].Remark
                lastinrec = TimeRecords.objects.filter(Date=date).filter(Barcode=barcode).filter(Type='O')
                if lastinrec:
                    lastin = lastinrec[0].Time
                    t1_m = lastin.hour*60 + lastin.minute
                    t2_m = time.hour*60 + time.minute
                    if t2_m - t1_m < 30:
                        message = str(user) + " already checked out"
                    else:
                        message = str(user) + " entry for today already marked"
                    return populate_user(request,message,'ams/barcode.html')        
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
        
        dayrule = DayRules.objects.filter(Date=date).filter(Barcode=barcode)
        if not dayrule:
            dayrule = DayRules.objects.filter(Date=date).filter(Category=category)
            if not dayrule:
                dayrule = DayRules.objects.filter(Date=date).filter(Category=CATEGORY_ALL)
                if not dayrule:         
                    dayrule = DayRules.objects.filter(Day=day).filter(Barcode=barcode)
                    if not dayrule:
                        dayrule = DayRules.objects.filter(Day=day).filter(Category=category)
                        if not dayrule:
                            dayrule = DayRules.objects.filter(Day=day).filter(Category=CATEGORY_ALL)
                    
        if dayrule:
            timerule = dayrule[0].Type

            if status == 'I':
                if timerule.Type == HOLIDAY_RULE:
                    remark = 'S'
                    attendance = Attendance()
                    attendance.Barcode = user
                    attendance.Date = date
                    attendance.Remark = remark
                    attendance.Year = AcademicYear.objects.filter(Status=1)[0]
                    attendance.save()
                    message = "Today is a holiday. Remember to checkout"
                    return populate_user(request,message,'ams/barcode.html')        
                
                t1_m = time.hour*60 + time.minute
                t2_m = timerule.HalfIn.hour*60 + timerule.HalfIn.minute
                if t1_m > t2_m + 15:
                    remark = 'A'
                elif time > timerule.LateIn:
                    tattendance = TempAttendance()
                    tattendance.Barcode = user
                    tattendance.Remark = 'L'
                    tattendance.save()
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
                                dayruleh = DayRules.objects.filter(Date=date).filter(Category=CATEGORY_ALL)
                                if not dayruleh:
                                    dayruleh = DayRules.objects.filter(Day=day).filter(Barcode=barcode)
                                    if not dayruleh:
                                        dayruleh = DayRules.objects.filter(Day=day).filter(Category=category)
                                        if not dayruleh:
                                            dayruleh = DayRules.objects.filter(Day=day).filter(Category=CATEGORY_ALL)
                                            
                        if (dayruleh) and (dayruleh[0].Type.Type == HOLIDAY_RULE):
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
                        attendance.Barcode = user
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
                        attendance.Barcode = user
                        attendance.Remark = rem
                        attendance.Date = date
                        attendance.Year = AcademicYear.objects.filter(Status=1)[0]
                        attendance.save()
                        
                        if time < timerule.HalfOut:
                            attendance = Attendance()
                            attendance.Barcode = user
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
                    tattendance = TempAttendance.objects.filter(Barcode=barcode)
                    if tattendance:
                        tattendance = tattendance[0]
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
                            attendance.Barcode = user
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
            message = "No day rule found. Contact administrator."
            
    return populate_user(request,message,'ams/barcode.html')        
    
#
@csrf_exempt
def populate_user(request,message,template):
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
    absentnoleave = []
    dt = datetime.datetime.now()
    date = dt.date()

    for usr in usersout:
        user_out = 0
        absent_remark = ''
        color = ''
        rem = ''
        attrcd = Attendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
        if attrcd:
            user_out = 1
            rem = attrcd[0].Remark
            if rem == 'O':
                absent_remark = 'OnLeave'
            elif rem == 'D':
                absent_remark = 'OnDuty'
            elif rem == 'C':
                absent_remark = 'Compensatory Off'
            if rem == 'F':
                leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
                if leaves:
                    lchoice = leaves[0].Type
                    if lchoice == 5:
                        absent_remark = 'First Half'
                    elif lchoice == 6:
                        absent_remark = 'Seconf Half'

        lattrcd = LeaveAttendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
        if lattrcd:
            rem = lattrcd[0].Remark
            if rem == 'O':
                absent_remark = 'OnLeave'
            elif rem == 'D':
                absent_remark = 'OnDuty'
            elif rem == 'C':
                absent_remark = 'Compensatory Off'
            if rem == 'F':
                leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
                if leaves:
                    lchoice = leaves[0].Type
                    if lchoice == 5:
                        absent_remark = 'First Half'
                    elif lchoice == 6:
                        absent_remark = 'Seconf Half'

        if absent_remark != '' and rem != 'F' and rem != 'D' and user_out == 1:
            color = 'red'

        if absent_remark != '':
            absent.append({'user': usr, 'remark': absent_remark, 'color':color})
        
        if user_out == 1:
            gone.append({'user': usr, 'color': color})

        if not attrcd and not lattrcd:
            yettocome.append({'user': usr})

    for usr in usersin:
        user_in = 0
        absent_remark = ''
        color = ''
        rem = ''
        attrcd = Attendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
        if attrcd:
            user_in = 1
            rem = attrcd[0].Remark
            if rem == 'O':
                absent_remark = 'OnLeave'
            elif rem == 'D':
                absent_remark = 'OnDuty'
            elif rem == 'C':
                absent_remark = 'Compensatory Off'
            if rem == 'F':
                leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
                if leaves:
                    lchoice = leaves[0].Type
                    if lchoice == 5:
                        absent_remark = 'First Half'
                    elif lchoice == 6:
                        absent_remark = 'Second Half'
        lattrcd = LeaveAttendance.objects.filter(Date=date).filter(Barcode=usr.Barcode)
        if lattrcd:
            rem = lattrcd[0].Remark
            if rem == 'O':
                absent_remark = 'OnLeave'
            elif rem == 'D':
                absent_remark = 'OnDuty'
            elif rem == 'C':
                absent_remark = 'Compensatory Off'
            if rem == 'F':
                leaves = Leaves.objects.filter(LeaveDate=date).filter(Barcode=usr.Barcode)
                if leaves:
                    lchoice = leaves[0].Type
                    if lchoice == 5:
                        absent_remark = 'First Half'
                    elif lchoice == 6:
                        absent_remark = 'Second Half'

        if absent_remark != '' and rem != 'F' and rem != 'D' and user_in == 1:
            color = 'red'

        if absent_remark != '':
            absent.append({'user': usr, 'remark': absent_remark, 'color':color})
        
        if user_in == 1:
            come.append({'user': usr, 'color': color})

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
    
    usersforgot = ForgotCheckout.objects.filter(Status=1).order_by('Date')      
    for usr in usersforgot:
        forgotcheckout.append({'user': usr})

    # Find pending requests for template ams/display.html
    pendingleaves = Leaves.objects.filter(Status=1).order_by('LeaveDate')
    leaves = []
    if pendingleaves:
        for pleave in pendingleaves:
            leaves.append({'leave':pleave})
            
    # Find absent remarks for which there is no corresponding leave request for template ams/display.html
    current_year = AcademicYear.objects.get(Status=1)
    absentremarks = Attendance.objects.filter(Remark__in=('A','H')).filter(Year=current_year).filter(Status__in=(1,2))
    for rem in absentremarks:
        leaverequest = Leaves.objects.filter(Barcode=rem.Barcode).filter(LeaveDate=rem.Date)
        if not leaverequest:
            absentnoleave.append({'remark':rem})
            
    return render_to_response(template,Context({'come': come,'yettocome':yettocome,'gone':gone,'absent':absent,
                                'forgotcheckout':forgotcheckout,'message':message,'jsdate': jsdate,'datestr': datestr,'leaves':leaves,
                                'absentnoleave':absentnoleave}))

#
@csrf_exempt
def ams_display(request):
    return populate_user(request,'','ams/display.html')
    
#
@csrf_exempt
def app_leave(request):
    message = "";
    disabled = 'true'
    user = 0

    if (not request.user.email) or (request.user.email == ""):
        form = LeaveForm()
        return render_to_response('ams/leaveapp.html', {'form': form})

    users = User.objects.filter(Email=request.user.email)
    if users:
        user = users[0]
            
    if request.user.is_superuser:
        disabled = 'false'
    
    if not request.POST:
        if user:
            form = LeaveForm({'Barcode':user.Barcode, 'Category':user.Category.Id, 'Type':1})
        else:
            form = LeaveForm()
        return render_to_response('ams/leaveapp.html', {'form': form, 'disabled':disabled})
    else:
        form = LeaveForm(request.POST)
        if not form.is_valid():
            return render_to_response('ams/leaveapp.html', {'form': form, 'disabled':disabled})
        if request.POST['applyforleave'] == '1':
            if form.is_valid():
                fdate = form.cleaned_data['FromDate']
                tdate = form.cleaned_data['ToDate']
                barcode = form.cleaned_data['Barcode']
                category = form.cleaned_data['Category']
                reason = form.cleaned_data['Reason']
                
                if (not fdate) or (not tdate):
                    message = "Please supply both the dates for leave application"
                    return render_to_response('ams/leaveapp.html', {'form': form, 'message': message, 'disabled':disabled})
                if fdate <= tdate:
                    date = fdate 
                    oneday = datetime.timedelta(1)
                    while 1:
                        day = date.isoweekday()
                        dayruleh = DayRules.objects.filter(Date=date).filter(Barcode=barcode.Barcode)
                        if not dayruleh:
                            dayruleh = DayRules.objects.filter(Date=date).filter(Category=category)
                            if not dayruleh:
                                dayruleh = DayRules.objects.filter(Date=date).filter(Category=CATEGORY_ALL)
                                if not dayruleh:
                                    dayruleh = DayRules.objects.filter(Day=day).filter(Barcode=barcode.Barcode)
                                    if not dayruleh:
                                        dayruleh = DayRules.objects.filter(Day=day).filter(Category=category)
                                        if not dayruleh:
                                            dayruleh = DayRules.objects.filter(Day=day).filter(Category=CATEGORY_ALL)
                                            
                        if (dayruleh) and (dayruleh[0].Type.Type == HOLIDAY_RULE):
                            pass
                        else:
                            prevapp = Leaves.objects.filter(LeaveDate=date).filter(Barcode=barcode)
                            if prevapp:
                                leaves = prevapp[0]
                                if leaves.Status == 2:
                                    if date < datetime.datetime.now().date():
                                        message = "Leave already approved!"
                                        return render_to_response('ams/leaveapp.html', {'form': form, 'message': message, 'disabled':disabled})
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
                    return render_to_response('ams/leaveapp.html', {'form': form, 'message': message, 'disabled':disabled})
                message = "Leave application submitted for user " + str(barcode)
        elif request.POST['applyforleave'] == '2':
            if form.is_valid():
                fdate = form.cleaned_data['FromDate']
                tdate = form.cleaned_data['ToDate']
                barcode = form.cleaned_data['Barcode']
                category = form.cleaned_data['Category']
                if (not fdate) or (not tdate):
                    message = "Please supply both the dates for leave cancellation"
                    return render_to_response('ams/leaveapp.html', {'form': form, 'message': message, 'disabled':disabled})
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
                    return render_to_response('ams/leaveapp.html', {'form': form, 'message': message, 'disabled':disabled})
                message = "Leave cancellation submitted for user " + str(barcode)
        elif request.POST['applyforleave'] == '3':
            if form.is_valid():
                days = form.cleaned_data['Days']            
                barcode = form.cleaned_data['Barcode']
                category = form.cleaned_data['Category']
                if not days:
                    message = "Please give no. of days for encashment!"             
                    return render_to_response('ams/leaveapp.html', {'form': form, 'message': message, 'disabled':disabled})
                enleave = EncashLeaves()
                enleave.Barcode = barcode
                enleave.Days = days
                enleave.Status = 1
                enleave.save()
                message = "Leave encashment submitted for user " + str(barcode)
                
        barcode = form.cleaned_data['Barcode']
        category = form.cleaned_data['Category']
        acadyear = AcademicYear.objects.get(Status=1)
        pendingleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=1).filter(LeaveDate__gte = acadyear.StartDate, LeaveDate__lte = acadyear.EndDate)
        approveleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=2).filter(LeaveDate__gte = acadyear.StartDate, LeaveDate__lte = acadyear.EndDate)
        usrdayrules = DayRules.objects.filter(Barcode=barcode.Barcode)
        catdayrules = DayRules.objects.filter(Category=barcode.Category).filter(Barcode__isnull=True)
        comdayrules = DayRules.objects.filter(Category=CATEGORY_ALL)
        appdaterules = []
        appdayrules = []
        timerules = []
        
        for rule in comdayrules:
            if rule.Date:
                if not catdayrules.filter(Date=rule.Date) and not usrdayrules.filter(Date=rule.Date):
                    appdaterules.append({'date': rule.Date, 'day': DAY_CHOICES[rule.Date.isoweekday()-1][1], 'type': rule.Type})
            elif rule.Day:
                if not catdayrules.filter(Day=rule.Day) and not usrdayrules.filter(Day=rule.Day):
                    appdayrules.append({'date': rule.Date, 'day': DAY_CHOICES[rule.Day - 1][1], 'type': rule.Type})

        for rule in catdayrules:
            if rule.Date:
                if not usrdayrules.filter(Date=rule.Date):
                    appdaterules.append({'date': rule.Date, 'day': DAY_CHOICES[rule.Date.isoweekday()-1][1], 'type': rule.Type})
            elif rule.Day:
                if not usrdayrules.filter(Day=rule.Day):
                    appdayrules.append({'date': rule.Date, 'day': DAY_CHOICES[rule.Day - 1][1], 'type': rule.Type})

        for rule in usrdayrules:
            if rule.Date:
                appdaterules.append({'date': rule.Date, 'day': DAY_CHOICES[rule.Date.isoweekday()-1][1], 'type': rule.Type})
            elif rule.Day:
                appdayrules.append({'date': rule.Date, 'day': DAY_CHOICES[rule.Day - 1][1], 'type': rule.Type})
            
        for rule in appdaterules:
            if timerules.count({'timerule': rule['type']}) == 0:
                timerules.append({'timerule': rule['type']})

        for rule in appdayrules:
            if timerules.count({'timerule': rule['type']}) == 0:
                timerules.append({'timerule': rule['type']})
            
        data = []
        balance = [0,0,0,0,0,0,0,0,0]
        carryforward = [0,0,0,0,0,0,0,0,0]
        currentleaves = [0,0,0,0,0,0,0,0,0]
        takenleaves = [0,0,0,0,0,0,0,0,0]
        for type in LEAVE_CHOICES:
            leavetype = type[0]
            lrule = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)
            if lrule:
                total = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)[0].Days
            else:
                total = 0
            currentleaves[leavetype] = total    
            lvbalance = LeavesBalance.objects.filter(Barcode=barcode).filter(Type=leavetype)
            if lvbalance:
                total += lvbalance[0].Days
                carryforward[leavetype] = lvbalance[0].Days
                
            pending = pendingleaves.filter(Type=leavetype).count()
            approve = approveleaves.filter(Type=leavetype).count()
            balance[leavetype] = total - approve - pending
            takenleaves[leavetype] = approve + pending
            data.append({'type':type[1], 'total':total, 'approve': approve, 'pending':pending, 'balance':total - approve - pending })

        approveenleaves = EncashLeaves.objects.filter(Barcode=barcode).filter(Status=2)
        pendingenleaves = EncashLeaves.objects.filter(Barcode=barcode).filter(Status=1)
        approveencash = 0
        pendingencash = 0
        for enleave in approveenleaves:
            approveencash += enleave.Days
        for enleave in pendingenleaves:
            pendingencash += enleave.Days
        data.append({'type':'Encashed', 'total':0, 'approve': approveencash, 'pending':pendingencash, 'balance':0 })
        
        datedata = []
        for type in LEAVE_CHOICES:
            pendingdates = []
            approvedates = []
            leavetype = type[0]
            pleaves = pendingleaves.filter(Type=leavetype)
            for leave in pleaves:
                pendingdates.append(leave.LeaveDate)
            aleaves = approveleaves.filter(Type=leavetype)
            for leave in aleaves:
                approvedates.append(leave.LeaveDate)
            datedata.append({'type':type[1], 'approve': approvedates, 'pending':pendingdates})
            
        adays = Attendance.objects.filter(Barcode=barcode).filter(Remark='A').filter(Year=acadyear)
        ldays = Attendance.objects.filter(Barcode=barcode).filter(Remark__in=('L','E')).filter(Year=acadyear)
        fdays = ForgotCheckout.objects.filter(Barcode=barcode).filter(Date__gte = acadyear.StartDate, Date__lte = acadyear.EndDate)
        hdays = Attendance.objects.filter(Barcode=barcode).filter(Remark='H').filter(Year=acadyear)
        abdays = []
        hfdays = []
        ltdays = []
        fcdays = []
        counts = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        absentdays = 0
        halfdays = 0
        forgotdays = 0
        latedays = 0
        for day in adays:
            if not Leaves.objects.filter(Barcode=barcode).filter(LeaveDate=day.Date).filter(Type__in=(1,2,3)):
                abdays.append({'date':day.Date})
                absentdays += 1
        for day in hdays:
            if not Leaves.objects.filter(Barcode=barcode).filter(LeaveDate=day.Date).filter(Type__in=(5,6)):
                hfdays.append({'date':day.Date})
                halfdays += 1
            
        for day in ldays:
            ltdays.append({'date':day.Date})
            counts[day.Date.month] += 1
            latedays += 1

        for day in fdays:
            fcdays.append({'date':day.Date})
            forgotdays += 1
        
        late = 0
        for cnt in counts:
            late = late + (cnt/3)
            
        total_subtract = ((late + halfdays + (-balance[5]) + (-balance[6])) / 2.0)  + absentdays
        if total_subtract > balance[1]:
            total_subtract -= balance[1]
            takenleaves[1] = carryforward[1] + currentleaves[1]
            takenleaves[3] += total_subtract
            balance[1] = 0
            balance[3] -= total_subtract
        else:
            balance[1] -= total_subtract
            takenleaves[1] += total_subtract

# Deduct encashed leaves from earned leave balance
        takenleaves[3] += (approveencash + pendingencash)
        balance[3] -= (approveencash + pendingencash)
        
        return render_to_response('ams/leaveapp.html', {'datedata':datedata,'form': form, 'data': data, 'message': message, 'abdays': abdays,
                                     'absentdays': absentdays, 'latedays': late, 'ltdays': ltdays, 'hfdays':hfdays, 'halfdays': halfdays,
                                     'balance': balance, 'carryforward': carryforward, 'currentleaves': currentleaves,
                                     'takenleaves': takenleaves, 'forgotdays': forgotdays, 'fcdays': fcdays, 'disabled':disabled,
                                     'dayrules':appdayrules, 'daterules':appdaterules, 'timerules':timerules})

#
@csrf_exempt
def monthly_report(request):
    message = ""
    if not request.POST:
        form = ReportForm()
        return render_to_response('ams/report.html', {'form': form})
    else:
        form = ReportForm(request.POST)
        if not form.is_valid():
            return render_to_response('ams/report.html', {'form': form})
        else:
            barcode = form.cleaned_data['Barcode']
            fdate = form.cleaned_data['FromDate']
            tdate = form.cleaned_data['ToDate']
            
            if fdate > tdate:
                message = "Please supply valid dates for monthly attendance"
                return render_to_response('ams/report.html', {'form': form, 'message': message})

            attendance = Attendance.objects.filter(Barcode=barcode).filter(Date__gte = fdate, Date__lte = tdate)
            timerecords = TimeRecords.objects.filter(Barcode=barcode).filter(Date__gte = fdate, Date__lte = tdate)
            
            oneday = datetime.timedelta(1)
            date = fdate
            report = []
            late = 0
            half = 0
            abs = 0
            while 1:
                day = date.strftime("%A")
                
                trin = timerecords.filter(Date=date).filter(Type='I')
                trout = timerecords.filter(Date=date).filter(Type='O')
                remark = attendance.filter(Date=date)
                
                if trin:
                    str1 = trin[0].Time.strftime("%H:%M:%S")
                else:
                    str1 = "NIL"    
                
                if trout:
                    str2 = trout[0].Time.strftime("%H:%M:%S")
                else:
                    str2 = "NIL"    
                
                if remark:
                    str3 = ""
                    for ar in remark:
                        tmp = ar.Remark
                        if tmp == 'A' or tmp == 'O':
                            abs += 1
                        if tmp == 'H' or tmp == 'F':
                            half += 1
                        if tmp == 'L' or tmp == 'E':
                            late += 1
                                
                        for tmprem in REMARK_CHOICES:
                            if tmp == tmprem[0]:
                                str3 = str3 + " " + tmprem[1]
                else:
                    str3 = "NIL"        
                
                report.append({'date':date,'day':day,'ti':str1,'to':str2,'rem':str3})
                
                date = date + oneday
                if date > tdate:
                    break
                    
                    
            return render_to_response('ams/report.html', {'form': form, 'message': message, 'report':report, 'late':late, 'half':half, 'absent':abs})       
                    
#
@csrf_exempt
def daily_report(request):
    message = ""
    if not request.POST:
        form = DailyReportForm()
        return render_to_response('ams/dailyreport.html', {'form': form})
    else:
        form = DailyReportForm(request.POST)
        if not form.is_valid():
            return render_to_response('ams/dailyreport.html', {'form': form})
        else:
            category = form.cleaned_data['Category']
            date = form.cleaned_data['Date']
            
            if category:
                users = User.objects.filter(Category=category)
            else:
                users = User.objects.all()
                
            report = []
            late = 0
            half = 0
            abs = 0
            for usr in users:
                remark = Attendance.objects.filter(Barcode=usr).filter(Date=date)
                timerecords = TimeRecords.objects.filter(Barcode=usr).filter(Date=date)

                trin = timerecords.filter(Type='I')
                trout = timerecords.filter(Type='O')
                
                if trin:
                    str1 = trin[0].Time.strftime("%H:%M:%S")
                else:
                    str1 = "NIL"    
                
                if trout:
                    str2 = trout[0].Time.strftime("%H:%M:%S")
                else:
                    str2 = "NIL"    
                
                if remark:
                    str3 = ""
                    for ar in remark:
                        tmp = ar.Remark
                        if tmp == 'A' or tmp == 'O':
                            abs += 1
                        if tmp == 'H' or tmp == 'F':
                            half += 1
                        if tmp == 'L' or tmp == 'E':
                            late += 1
                                
                        for tmprem in REMARK_CHOICES:
                            if tmp == tmprem[0]:
                                str3 = str3 + " " + tmprem[1]
                else:
                    str3 = "NIL"        
                
                report.append({'user':usr,'ti':str1,'to':str2,'rem':str3})

            return render_to_response('ams/dailyreport.html', {'form': form, 'message': message, 'report':report,
                                     'late':late, 'half':half, 'absent':abs, 'date':date})      

#
@csrf_exempt
def report_leave(request):
    message = "";
    disabled = 'true'
    user = 0

    if (not request.user.email) or (request.user.email == ""):
        form = LeaveReportForm()
        return render_to_response('ams/leavereport.html', {'form': form})

    users = User.objects.filter(Email=request.user.email)
    if users:
        user = users[0]
            
    if request.user.is_superuser:
        disabled = 'false'
    
    if not request.POST:
        if user:
            form = LeaveReportForm({'Barcode':user.Barcode, 'Category':user.Category.Id})
        else:
            form = LeaveReportForm()
        return render_to_response('ams/leavereport.html', {'form': form, 'disabled':disabled})
    else:
        form = LeaveReportForm(request.POST)
        if not form.is_valid():
            return render_to_response('ams/leavereport.html', {'form': form, 'disabled':disabled})

        barcode = form.cleaned_data['Barcode']
        category = form.cleaned_data['Category']
        acadyear = AcademicYear.objects.get(Status=1)

        ams_users = []
        if barcode:
            ams_users.append(barcode)
        elif (category == CATEGORY_ALL):
            ams_users = User.objects.all()
        else:
            ams_users = User.objects.filter(Category = category)

        data = []

        for usr in ams_users:
            barcode = usr
            category = usr.Category
            pendingleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=1).filter(LeaveDate__gte = acadyear.StartDate, LeaveDate__lte = acadyear.EndDate)
            approveleaves = Leaves.objects.filter(Barcode=barcode).filter(Status=2).filter(LeaveDate__gte = acadyear.StartDate, LeaveDate__lte = acadyear.EndDate)
            balance = [0,0,0,0,0,0,0,0,0]
            carryforward = [0,0,0,0,0,0,0,0,0]
            currentleaves = [0,0,0,0,0,0,0,0,0]
            takenleaves = [0,0,0,0,0,0,0,0,0]
            for type in LEAVE_CHOICES:
                leavetype = type[0]
                lrule = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)
                if lrule:
                    total = LeaveRules.objects.filter(Category=category).filter(Type=leavetype)[0].Days
                else:
                    total = 0
                currentleaves[leavetype] = total    
                lvbalance = LeavesBalance.objects.filter(Barcode=barcode).filter(Type=leavetype)
                if lvbalance:
                    total += lvbalance[0].Days
                    carryforward[leavetype] = lvbalance[0].Days
                    
                pending = pendingleaves.filter(Type=leavetype).count()
                approve = approveleaves.filter(Type=leavetype).count()
                balance[leavetype] = total - approve - pending
                takenleaves[leavetype] = approve + pending
    
            approveenleaves = EncashLeaves.objects.filter(Barcode=barcode).filter(Status=2)
            pendingenleaves = EncashLeaves.objects.filter(Barcode=barcode).filter(Status=1)
            approveencash = 0
            pendingencash = 0
            for enleave in approveenleaves:
                approveencash += enleave.Days
            for enleave in pendingenleaves:
                pendingencash += enleave.Days
            #data.append({'type':'Encashed', 'total':0, 'approve': approve, 'pending':pending, 'balance':0 })
            
            adays = Attendance.objects.filter(Barcode=barcode).filter(Remark='A').filter(Year=acadyear)
            ldays = Attendance.objects.filter(Barcode=barcode).filter(Remark__in=('L','E')).filter(Year=acadyear)
            fdays = ForgotCheckout.objects.filter(Barcode=barcode).filter(Date__gte = acadyear.StartDate, Date__lte = acadyear.EndDate)
            hdays = Attendance.objects.filter(Barcode=barcode).filter(Remark='H').filter(Year=acadyear)
            counts = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            absentdays = 0
            halfdays = 0
            forgotdays = 0
            latedays = 0
            for day in adays:
                if not Leaves.objects.filter(Barcode=barcode).filter(LeaveDate=day.Date).filter(Type__in=(1,2,3)):
                    absentdays += 1
            for day in hdays:
                if not Leaves.objects.filter(Barcode=barcode).filter(LeaveDate=day.Date).filter(Type__in=(5,6)):
                    halfdays += 1
                
            for day in ldays:
                counts[day.Date.month] += 1
                latedays += 1
    
            for day in fdays:
                forgotdays += 1
            
            late = 0
            for cnt in counts:
                late = late + (cnt/3)
                
            total_subtract = ((late + halfdays + (-balance[5]) + (-balance[6])) / 2.0)  + absentdays
            if total_subtract > balance[1]:
                total_subtract -= balance[1]
                takenleaves[1] = carryforward[1] + currentleaves[1]
                takenleaves[3] += total_subtract
                balance[1] = 0
                balance[3] -= total_subtract
            else:
                balance[1] -= total_subtract
                takenleaves[1] += total_subtract
            
    # Deduct encashed leaves from earned leave balance
            takenleaves[3] += (approveencash + pendingencash)
            balance[3] -= (approveencash + pendingencash)

            data.append({'usr':barcode, 'casualtaken':takenleaves[1], 'casualbal':balance[1], 
                            'sicktaken':takenleaves[2], 'sickbal':balance[2], 'earnedtaken':takenleaves[3], 'earnedbal':balance[3],
                            'absent': absentdays, 'half':halfdays, 'late':latedays, 'forgot':forgotdays})
                    
        return render_to_response('ams/leavereport.html', {'form': form, 'data': data, 'message': message, 'disabled':disabled})

#
@csrf_exempt
def add_dayrules(request):
    message = "";
    if not request.POST:
        form = DayRulesForm()
        return render_to_response('ams/dayrules.html', {'form': form})
    else:
        form = DayRulesForm(request.POST)
        if not form.is_valid():
            return render_to_response('ams/dayrules.html', {'form': form})
        if request.POST['addrules'] == '1':
            if form.is_valid():
                fdate = form.cleaned_data['FromDate']
                tdate = form.cleaned_data['ToDate']
                barcode = form.cleaned_data['Barcode']
                category = form.cleaned_data['Category']
                timerule = form.cleaned_data['Type']

                if not timerule:
                    message = "Please supply time rule for adding dayrule"
                    return render_to_response('ams/dayrules.html', {'form': form, 'message': message})
                if (not barcode) and (not category):
                    message = "Please supply category and/or user for adding dayrule"
                    return render_to_response('ams/dayrules.html', {'form': form, 'message': message})
                if (not fdate) or (not tdate):
                    message = "Please supply both the dates for adding dayrule"
                    return render_to_response('ams/dayrules.html', {'form': form, 'message': message})
                if fdate <= tdate:
                    date = fdate 
                    oneday = datetime.timedelta(1)
                    while 1:
                        dayrule = DayRules()
                        if category:
                            dayrule.Category = category
                        if barcode:
                            dayrule.Barcode = barcode.Barcode
                        dayrule.Date = date
                        dayrule.Type = timerule
                        dayrule.save()
                        
                        date = date + oneday
                        if date > tdate:
                            break
                else:
                    message = "Enter correct dates!"
                return render_to_response('ams/dayrules.html', {'form': form, 'message': message})
        elif request.POST['addrules'] == '2':
            if form.is_valid():
                fdate = form.cleaned_data['FromDate']
                tdate = form.cleaned_data['ToDate']
                barcode = form.cleaned_data['Barcode']
                category = form.cleaned_data['Category']
                
                if (not fdate) or (not tdate):
                    message = "Please supply both the dates for displaying dayrule"
                    return render_to_response('ams/dayrules.html', {'form': form, 'message': message})
                
                dater = []
                dayr = []
                categories = []
                if (not barcode) and (not category):
                    categories = Category.objects.all()
                elif barcode:
                    categories = Category.objects.filter(Id=barcode.Category.Id)
                else:
                    categories = Category.objects.filter(Id=category.Id)
                    
                    
                if fdate <= tdate:
                    for cat in categories:
                        date = fdate 
                        oneday = datetime.timedelta(1)
                        today = datetime.datetime.now().date()
                        while 1:
                            day = date.isoweekday()
                            if barcode:
                                daterules = DayRules.objects.filter(Date=date).filter(Barcode=barcode.Barcode)
                                if daterules:
                                    dater.append({'dater':daterules[0], 'daystr':DAY_CHOICES[day-1][1]})

                            daterules = DayRules.objects.filter(Date=date).filter(Category=cat)
                            if daterules:
                                dater.append({'dater':daterules[0], 'daystr':DAY_CHOICES[day-1][1]})
                
                            if barcode:
                                dayrules = DayRules.objects.filter(Day=day).filter(Barcode=barcode.Barcode)
                                if dayrules:
                                    dayr.append({'dayr':dayrules[0], 'daystr':DAY_CHOICES[day-1][1]})

                            dayrules = DayRules.objects.filter(Day=day).filter(Category=cat)
                            if dayrules:
                                dayr.append({'dayr':dayrules[0], 'daystr':DAY_CHOICES[day-1][1]})
    
                            date = date + oneday
                            if date > tdate:
                                break
                    return render_to_response('ams/dayrules.html', {'form': form, 'message': message, 'dayrules':dayr, 'daterules':dater})
                else:
                    message = "Enter correct dates!"
                    return render_to_response('ams/dayrules.html', {'form': form, 'message': message})
        else:
            message = "Invalid option."
            return render_to_response('ams/dayrules.html', {'form': form, 'message': message})

#
@csrf_exempt
def admin_home(request):
    user = request.user
    if user.is_superuser:
        print "superuser"
    else:
        print "not superuser"
        

ams_display = login_required(ams_display)
app_leave = login_required(app_leave)
daily_report = login_required(daily_report)
monthly_report = login_required(monthly_report)
report_leave = login_required(report_leave)
