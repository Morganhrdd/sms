from django.db.models import Q, Max
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
from jp_sms.pravesh.models import ApplicationForm, GenerateHallTicketForm
from jp_sms.pravesh.models import HallTicket, Session, ClassRoom, Student
# Create your views here.

MEDIUM = {'E':'English', 'M':'Marathi'}

def add(request):
    print get_seatnumber()
    if not request.POST:
        applicationform = ApplicationForm()
        return render_to_response('pravesh/add.html', {'form': applicationform})
    else:
        applicationform = ApplicationForm(request.POST)
        if not applicationform.is_valid():
            return render_to_response('pravesh/add.html', {'form': applicationform})
        if request.POST['PayMode'] == 'DD' and not request.POST['DDNo']:
            return render_to_response('pravesh/add.html', {'form': applicationform, 'message':'DD Number is mandatory'})
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
        hallticket_obj = HallTicket()
        hallticket_obj.Student = student_obj
        hallticket_obj.Session = get_session(medium=student_obj.Medium)
        hallticket_obj.ClassRoom = get_classroom(session_obj=hallticket_obj.Session, medium=student_obj.Medium)
        hallticket_obj.SeatNumber = get_seatnumber()
        print "HALLTICKET", hallticket_obj
        hallticket_obj.save()
        return render_to_response('pravesh/add.html', {'form':applicationform, 'message':'Successfully added %s' % (student_obj.FirstName)})


def display_hallticket(request, seatnumber):
    hallticket_obj = HallTicket.objects.filter(SeatNumber=seatnumber)
    print hallticket_obj
    try:
        hallticket_obj = HallTicket.objects.get(SeatNumber=seatnumber)
        data = {}
        data['firstname'] = hallticket_obj.Student.FirstName
        data['middlename'] = hallticket_obj.Student.MiddleName
        data['lastname'] = hallticket_obj.Student.LastName
        data['hall_id'] = ' %s-%s-%s' % (hallticket_obj.Session.Number, hallticket_obj.ClassRoom.Number, hallticket_obj.SeatNumber)
        data['medium'] = MEDIUM[hallticket_obj.Student.Medium]
        data['date'] = hallticket_obj.Session.Start.strftime('%d-%b-%Y')
        data['session'] = hallticket_obj.Session.Name
        data['session_time'] = '%s to %s' % (hallticket_obj.Session.Start.strftime('%H:%M'), hallticket_obj.Session.End.strftime('%H:%M'))
        return render_to_response('pravesh/hallticket.html', {'data':data})
    except:
        return render_to_response('pravesh/hallticket.html', {'msg': 'Seat number [<i>%s</i>] does not exists' % (seatnumber)})

def index(request):
    data = {}
    data['add_url'] = '/pravesh/add'
    data['generate_hallticket_url'] = '/pravesh/generate_hallticket'
    return render_to_response('pravesh/index.html',{'data':data})
    

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

def get_seatnumber():
    tmp = HallTicket.objects.aggregate(Max('SeatNumber'))
    tmp = tmp['SeatNumber__max']
    if tmp == None: tmp = 0
    return tmp+1
    tmp = HallTicket.objects.all()
    maxval = 0
    for x in tmp:
        if maxval < int(x.SeatNumber):
            maxval = int(x.SeatNumber)
    return str(maxval+1)

def get_classroom(session_obj=None, medium=None):
    retval = {}
    for classroom in session_obj.classrooms.all():
        if classroom.Medium != medium:
            continue
        retval[classroom.Number] = {}
        retval[classroom.Number]['Capacity'] = classroom.Capacity
        retval[classroom.Number]['Current'] = len(HallTicket.objects.filter(ClassRoom__Number=classroom.Number, Session=session_obj))
    tmp = retval.keys()
    tmp.sort()
    for k in tmp:
        if retval[k]['Current'] < retval[k]['Capacity']:
            return ClassRoom.objects.get(Number=k)
    return None


def get_session(medium=None):
    session_objs = Session.objects.all()
    for session_obj in session_objs:
        if get_classroom(session_obj=session_obj, medium=medium):
            return session_obj
    return None
    pass