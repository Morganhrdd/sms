from django.db.models import Q, Count
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from jp_sms.pravesh.models import ApplicationForm, GenerateHallTicketForm
from jp_sms.pravesh.models import HallTicket, Session, ClassRoom, Student

# Create your views here.

import httplib
import datetime
import urllib
import logging

LOG_FILENAME = '/tmp/sms.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MEDIUM = {'E':'English', 'M':'Marathi'}

def sms_send(user=None, password=None, senderid=None, nos=None, msg=None, schedule=None):
    for no in nos:
        params = urllib.urlencode({'user': user, 'pwd': password, 'senderid': senderid, 'mobileno':str(no), 'msgtext': msg, 'priority':'High'})
        conn = httplib.HTTPConnection('bulksmsindia.mobi', 80, timeout=10)
        conn.request("GET", "/sendurl.asp?%s"%(params))
        response = conn.getresponse()
        logging.debug('Number: %s, Status: %s, Reason: %s, Output: %s' % (no, response.status, response.reason, response.read()))
        conn.close()
        
def add(request):
    if not request.POST:
        applicationform = ApplicationForm()
        return render_to_response('pravesh/add.html', {'form': applicationform, 'button_name':'Add'})
    else:
        applicationform = ApplicationForm(request.POST)
        if not applicationform.is_valid():
            return render_to_response('pravesh/add.html', {'form': applicationform, 'button_name':'Add'})
        if request.POST['PayMode'] == 'DD' and not request.POST['DDNo']:
            return render_to_response('pravesh/add.html', {'form': applicationform, 'message':'DD Number is mandatory', 'button_name':'Add'})
        if request.POST.has_key('edit'):
            student_obj = Student(pk=request.POST['edit'])
        else:
            student_obj = Student()
        student_obj.FirstName = request.POST['FirstName']
        student_obj.MiddleName = request.POST['MiddleName']
        student_obj.LastName = request.POST['LastName']
        student_obj.FatherName = request.POST['FatherName']
        student_obj.MotherName = request.POST['MotherName']
        student_obj.Address = request.POST['Address']
        student_obj.Pincode = int(request.POST['Pincode'])
        student_obj.PhoneHome = request.POST['PhoneHome']
        student_obj.PhoneMobile = request.POST['PhoneMobile']
        student_obj.Email = request.POST['Email']
        student_obj.Medium = request.POST['Medium']
        student_obj.Gender = request.POST['Gender']
        student_obj.DateOfBirth = request.POST['DateOfBirth']
        student_obj.CurrentSchool = request.POST['CurrentSchool']
        student_obj.CurrentStd = 0
        if request.POST['CurrentStd']:
            student_obj.CurrentStd = int(request.POST['CurrentStd'])
        student_obj.PayMode = request.POST['PayMode']
        student_obj.DDNo = request.POST['DDNo']
        student_obj.save()
        x = get_seatnumber(medium=student_obj.Medium)
        if not request.POST.has_key('edit'):
            hallticket_obj = HallTicket()
            hallticket_obj.Student = student_obj
            hallticket_obj.ClassRoom = ClassRoom.objects.get(pk=x['classroom'])
            hallticket_obj.SeatNumber = x['seatnumber']
            hallticket_obj.save()
            return redirect('/pravesh/hallticket/%s'%(hallticket_obj.pk))
        return redirect('/pravesh')
#
def edit(request, pk):
    try:
        student_obj = Student.objects.get(pk=pk)
        data = {}
        data['FirstName'] = student_obj.FirstName
        data['MiddleName'] = student_obj.MiddleName
        data['LastName'] = student_obj.LastName
        data['FatherName'] = student_obj.FatherName
        data['MotherName'] = student_obj.MotherName
        data['Address'] = student_obj.Address
        data['Pincode'] = student_obj.Pincode
        data['PhoneHome'] = student_obj.PhoneHome
        data['PhoneMobile'] = student_obj.PhoneMobile
        data['Email'] = student_obj.Email
        data['Medium'] = student_obj.Medium
        data['Gender'] = student_obj.Gender
        data['DateOfBirth'] = student_obj.DateOfBirth
        data['CurrentSchool'] = student_obj.CurrentSchool
        data['CurrentStd'] = student_obj.CurrentStd
        data['PayMode'] = student_obj.PayMode
        data['DDNo'] = student_obj.DDNo
        applicationform = ApplicationForm(initial=data)
        return render_to_response('pravesh/add.html', {'form':applicationform, 'button_name':'Update', 'edit':student_obj.pk})
    except:
        return render_to_response('pravesh/add.html', {'message':'Record not found'})
    try:
        hallticket_obj = HallTicket.objects.filter(pk=pk)
        applicationform = ApplicationForm()
        applicationform.FirstName = hallticket_obj.Student.FirstName
        return render_to_response('pravesh/add.html', {'form':applicationform})
    except:
        return redirect('/pravesh/')


def display_hallticket(request, pk):
    try:
        hallticket_obj = HallTicket.objects.get(pk=pk)
        data = {}
        data['firstname'] = hallticket_obj.Student.FirstName
        data['middlename'] = hallticket_obj.Student.MiddleName
        data['lastname'] = hallticket_obj.Student.LastName
        data['hall_id'] = '%s%s-%s' % (hallticket_obj.ClassRoom.Medium, hallticket_obj.ClassRoom.Number, hallticket_obj.SeatNumber)
        data['classroom'] = hallticket_obj.ClassRoom.Name
        data['medium'] = MEDIUM[hallticket_obj.Student.Medium]
        data['date'] = hallticket_obj.ClassRoom.Session.Start.strftime('%d-%b-%Y')
        data['session'] = hallticket_obj.ClassRoom.Session.Name
        data['session_time'] = '%s to %s' % (hallticket_obj.ClassRoom.Session.Start.strftime('%H:%M'), hallticket_obj.ClassRoom.Session.End.strftime('%H:%M'))
        return render_to_response('pravesh/hallticket.html', {'data':data})
    except:
        return render_to_response('pravesh/hallticket.html', {'msg': 'Seat number [<i>%s</i>] does not exists' % (pk)})

def index(request):
    data = {}
    data['stats'] = {}
    data['stats']['MM'] = Student.objects.filter(Gender='M', Medium='M').aggregate(Count('Gender'))['Gender__count']
    data['stats']['ME'] = Student.objects.filter(Gender='M', Medium='E').aggregate(Count('Gender'))['Gender__count']
    data['stats']['FM'] = Student.objects.filter(Gender='F', Medium='M').aggregate(Count('Gender'))['Gender__count']
    data['stats']['FE'] = Student.objects.filter(Gender='F', Medium='E').aggregate(Count('Gender'))['Gender__count']
    data['stats']['MMFM'] = data['stats']['MM'] + data['stats']['FM']
    data['stats']['MEFE'] = data['stats']['ME'] + data['stats']['FE']
    data['stats']['MMME'] = data['stats']['MM'] + data['stats']['ME']
    data['stats']['FMFE'] = data['stats']['FM'] + data['stats']['FE']
    data['stats']['MMMEFMFE'] = data['stats']['MMME'] + data['stats']['FMFE']
    data['add_url'] = '/pravesh/add'
    data['generate_hallticket_url'] = '/pravesh/generate_hallticket'
    data['generate_report_url'] = '/pravesh/generate_report'
    return render_to_response('pravesh/index.html',{'data':data})
    

def edit_hallticket(request, seatnumber):
    if not request.POST:
        genform = GenerateHallTicketForm()
        return render_to_response('pravesh/generate_hallticket.html',{'form':genform})
    data = {}
    if request.POST['FirstName']:
        data['Student__FirstName__icontains'] = request.POST['FirstName']
    if request.POST['LastName']:
        data['Student__LastName__icontains'] = request.POST['LastName']
    hallticket_objs = HallTicket.objects.filter(**data)
    
def generate_hallticket(request):
    genform = GenerateHallTicketForm()
    if not request.POST:
        return render_to_response('pravesh/generate_hallticket.html',{'form':genform})
    data = {}
    if request.POST['FirstName']:
        data['Student__FirstName__icontains'] = request.POST['FirstName']
    if request.POST['LastName']:
        data['Student__LastName__icontains'] = request.POST['LastName']
    hallticket_objs = HallTicket.objects.filter(**data)
    if len(hallticket_objs):
        return render_to_response('pravesh/generate_hallticket.html', {'form':genform, 'hallticket_objs':hallticket_objs})
    return render_to_response('pravesh/generate_hallticket.html', {'form':genform})


def get_seatnumber(medium=None):
    session_objs = Session.objects.all().order_by('Number', 'pk')
    data = {}
    for session_obj in session_objs:
        data[session_obj.pk] =  {}
        classroom_objs = ClassRoom.objects.filter(Session=session_obj, Medium=medium).order_by('Number','pk')
        for classroom_obj in classroom_objs:
            data[session_obj.pk][classroom_obj.pk] = {}
            data[session_obj.pk][classroom_obj.pk]['Capacity'] = classroom_obj.Capacity
            data[session_obj.pk][classroom_obj.pk]['Current'] = len(HallTicket.objects.filter(ClassRoom=classroom_obj))
    retval = {}
    sessions = data.keys()
    sessions.sort()
    for s in sessions:
        #retval['session'] = s
        classrooms = data[s].keys()
        classrooms.sort()
        for c in classrooms:
            retval['classroom'] = c
            if data[s][c]['Current'] < data[s][c]['Capacity']:
                retval['seatnumber'] = data[s][c]['Current']+1
                return retval
    raise Exception("ERROR")

def generate_classreport(request):
    try:
        medium = request.GET['medium']
        number = request.GET['number']
        data = HallTicket.objects.filter(ClassRoom__Medium = medium, ClassRoom__Number = number).order_by('SeatNumber')
        return render_to_response('pravesh/display_report.html', {'data':data})
    except:
        data = ClassRoom.objects.all()
        return render_to_response('pravesh/display_report.html', {'classrooms':data})
add = login_required(add)
display_hallticket = login_required(display_hallticket)
generate_hallticket = login_required(generate_hallticket)
index = login_required(index)
generate_classreport = login_required(generate_classreport)