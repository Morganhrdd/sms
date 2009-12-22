from django.db.models import Q, Max
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import Context
from django.template.loader import get_template
from jp_sms.pravesh.models import ApplicationForm, HallTicket, Session, ClassRoom
# Create your views here.


def add(request):
    print get_session(medium='M')
    session_obj = Session.objects.get(Number=1)
    print get_classroom(session_obj, medium='M')
    if not request.POST:
        applicationform = ApplicationForm()
        return render_to_response('pravesh/add.html', {'form': applicationform})
    else:
        applicationform = ApplicationForm(request.POST)
        if not applicationform.is_valid():
            return render_to_response('pravesh/add.html', {'form': applicationform})
        if request.POST['PayMode'] == 'DD' and not request.POST['DDNo']:
            return render_to_response('pravesh/add.html', {'form': applicationform, 'message':'DD Number is mandatory'})
        return render_to_response('pravesh/add.html')

def get_seatnumber():
    tmp = HallTicket.objects.aggregate(Max('SeatNumber'))
    tmp = tmp['SeatNumber__max']
    if tmp == None: tmp = 0
    return tmp+1

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