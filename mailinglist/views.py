# Create your views here.
from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from sms.mailinglist.models import *
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required


from pprint import pprint

def display(request):
    respage = 'mailinglist/display.html'
    persons = generate_person_pages_list(html_brk = '<br />')
    return render_to_response(respage,{'persons':persons}, context_instance=RequestContext(request))

def generate_person_pages_list(max_rows=25, max_cols=4, html_brk = ''):
    persons = []
    max_cols = 4
    max_rows = 25
    cols = []
    col = 0
    row = 0
    col_str = ''
    for x in Person.objects.all():
        tmp = []
        tmp.append((x.Name))
        tmp.append((x.Address))
        tmp.append((x.City))
        tmp.append((x.Taluka))
        tmp.append((x.PinCode))
        tmp.append((x.District))
        tmp.append((x.Phone))
        tmp.append('<hr>')
        tmp_str = '\n'.join(tmp)
        if max_rows > row + len(col_str.split('\n')):
            col_str += tmp_str
            row += len(col_str.split('\n'))
            #cols.append(col_str.replace(u'\r\n',u'\n').replace(u'\n','\n'+html_brk)+html_brk)
        else:
            cols.append(col_str.replace(u'\r\n',u'\n').replace(u'\n','\n'+html_brk)+html_brk)
            col_str = ''
            col_str += '\n'.join(tmp) + '\n'
            col += 1
            row = 0
        if col >= max_cols:
            persons.append(cols)
            cols = []
            col = 0
            row = 0
    if col_str:
        cols.append('1'+col_str.replace(u'\r\n',u'\n').replace(u'\n','\n'+html_brk)+html_brk)
    if cols:
        persons.append(cols)
    return persons

display = login_required(display)
