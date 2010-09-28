# Create your views here.

from django.db.models import Q
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse 
from django.template import Context, RequestContext
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle,Frame,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import datetime
from array import array
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from sms.fees.models import *
from sms.fees.num2word_EN import Num2Word_EN


def fee_valid_user(user):
    if user.is_superuser:
        return True
    else:
        return False


#
def fee_receipt(request):
    if not fee_valid_user(request.user):
        return redirect('/')
    message = ""
    dt = datetime.datetime.now()
    date = dt.date()
    receiptnumber = "------"
    if not request.POST:
        form = FeeForm()
        return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber}, context_instance=RequestContext(request))
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
                    
                for classmaster in cms:
                    studentyearlyinfo = StudentYearlyInformation.objects.filter(StudentBasicInfo=student).filter(ClassMaster=classmaster)
                    if studentyearlyinfo:                
                        break
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
                    specialfeeqs = ScholarshipOrFee.objects.filter(StudentYearlyInformation=studentyearlyinfo[0]).filter(Type=2)
                    if specialfeeqs:
                        for specialfee in specialfeeqs:
                            if specialfee.FeeType.Type == feetype:
                                ftype = specialfee.FeeType
                                break
                    
                    if not ftype:
                        message = "Invalid Fee Type"
                        return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })
                else:
                    ftype = ftypes[0]
                                        
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
                feereceipt.FeeType = ftype
                feereceipt.Amount = amount
                feereceipt.ChequeNo = cheque
                feereceipt.Bank = bank
                feereceipt.Status = 1
                feereceipt.save()
                message = "Fee receipt " + str(feereceipt.ReceiptNumber) + " generated"
                receiptnumber = feereceipt.ReceiptNumber
                
                return print_receipt(feereceipt)
                
        elif request.POST['applyforfee'] == '0':
            if form.is_valid():
                regno = form.cleaned_data['RegNo']
                studentbi = StudentBasicInfo.objects.filter(RegistrationNo=regno)
                if not studentbi:
                    message = "Invalid Registration Number"
                    return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })                    
                student = studentbi[0]

                years = []
                classmaster = StudentYearlyInformation.objects.filter(StudentBasicInfo=student).order_by('-ClassMaster__Standard')
                if classmaster:
                    for data in classmaster:
                        hostel = data.Hostel
                        feetypes = FeeType.objects.filter(ClassMaster=data.ClassMaster)
                        feeinfo = []
                        if feetypes:
                            for ftype in feetypes:
                                tschol = 0
                                tspecialfee = 0
                                amount = ftype.Amount
                                if ftype.Type == 'Hostel':
                                    if hostel == 1:
                                        continue
                                    elif hostel == 3:
                                        amount = amount / 2
                                feereceipts = FeeReceipt.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype).filter(Status=1)
                                feedateamount = []
                                total = 0
                                if feereceipts:
                                    for fr in feereceipts:
                                        feedateamount.append({'ReceiptNo':fr.ReceiptNumber, 'Date':fr.Date, 'Amount':fr.Amount})
                                        total += fr.Amount
                                scholarshipqs = ScholarshipOrFee.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype)
                                if scholarshipqs:
                                    for schol in scholarshipqs:
                                        if schol.Type == 1:
                                            tschol += schol.Amount
                                        else:
                                            tspecialfee += schol.Amount

                                scholarship = []
                                specialfee = []
                                if tschol > 0:
                                    #total += tschol
                                    scholarship.append({'Amount': tschol})
                                if tspecialfee > 0:
                                    specialfee.append({'Amount': tspecialfee})

                                if tschol > 0 or tspecialfee > 0:
                                    feeinfo.append({'Type':ftype.Type, 'Amount':amount, 'FeeDateAmount': feedateamount, 'Total':total,
                                        'Balance':amount - total + tspecialfee - tschol, 'Scholarship': scholarship, 'SpecialFee': specialfee})
                                else:
                                    feeinfo.append({'Type':ftype.Type, 'Amount':amount, 'FeeDateAmount': feedateamount, 'Total':total,
                                        'Balance':amount - total})

                        specialfeeqs = ScholarshipOrFee.objects.filter(StudentYearlyInformation=data).filter(Type=2)
                        if specialfeeqs:
                            for specialfee in specialfeeqs:
                                ftype = specialfee.FeeType
                                amount = specialfee.Amount
                                total = 0
                                feereceipts = FeeReceipt.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype).filter(Status=1)
                                feedateamount = []
                                total = 0
                                if feereceipts:
                                    for fr in feereceipts:
                                        feedateamount.append({'ReceiptNo':fr.ReceiptNumber, 'Date':fr.Date, 'Amount':fr.Amount})
                                        total += fr.Amount
                                feeinfo.append({'Type':ftype.Type, 'Amount':amount, 'FeeDateAmount': feedateamount, 'Total':total,
                                    'Balance':amount - total})

                        years.append({'ClassMaster':data.ClassMaster, 'FeeInfo': feeinfo})                                                            

                return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,
                                            'receiptnumber':receiptnumber, 'student':student, 'years':years })                    

#
def fee_report(request):
    message = ""
    STYLE_OPEN_TAG = '<b>'
    STYLE_CLOSE_TAG = '</b>'
    if not request.POST:
        form = FeeReportForm()
        return render_to_response('fees/feereport.html', {'form': form, 'message': message})
    else:
        form = FeeReportForm(request.POST)
        if form.is_valid():
            div = form.cleaned_data['Division']
            year = form.cleaned_data['Year']
            std = form.cleaned_data['Std']
            show = form.cleaned_data['Show']
            cms = ClassMaster.objects.filter(AcademicYear=year)
            if std:
                cms = cms.filter(Standard=std)
            if div != 'A':
                cms = cms.filter(Division=div)

            students = []
            if not cms:
                message = "No matching records found!"
                return render_to_response('fees/feereport.html', {'form': form, 'message': message})
            else:
                studentsfound = 0
                for cm in cms.all():
                    studentinfo = StudentYearlyInformation.objects.filter(ClassMaster=cm)
                    if studentinfo:
                        studentsfound = 1
                        for data in studentinfo:
                            hostel = data.Hostel
                            feetypes = FeeType.objects.filter(ClassMaster=data.ClassMaster)
                            feeinfo = []
                            defaulter = 0
                            style_opentag = ''
                            style_closetag = ''
                            if feetypes:
                                for ftype in feetypes:
                                    tschol = 0
                                    tspecialfee = 0
                                    fstyle_opentag = ''
                                    fstyle_closetag = ''
                                    amount = ftype.Amount
                                    if ftype.Type == 'Hostel':
                                        if hostel == 1:
                                            continue
                                        elif hostel == 3:
                                            amount = amount / 2
                                    feereceipts = FeeReceipt.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype).filter(Status=1)
                                    total = 0
                                    receipts = []
                                    if feereceipts:
                                        for fr in feereceipts:
                                            total += fr.Amount
                                            receipts.append({'receipt': fr})
                                    balance = amount - total
                                    scholarship = ScholarshipOrFee.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype)
                                    if scholarship:
                                        for schol in scholarship:
                                            if schol.Type == 1:
                                                tschol += schol.Amount
                                            else:
                                                tspecialfee += schol.Amount
                                    balance += tspecialfee
                                    balance -= tschol
                                    if balance > 0:
                                        defaulter = 1
                                        style_opentag = STYLE_OPEN_TAG
                                        style_closetag = STYLE_CLOSE_TAG
                                        fstyle_opentag = STYLE_OPEN_TAG
                                        fstyle_closetag = STYLE_CLOSE_TAG
                                    feeinfo.append({'Type':ftype.Type, 'Amount':amount, 'Total':total,
                                        'Balance':balance, 'FStyleOpenTag':fstyle_opentag, 'FStyleCloseTag':fstyle_closetag,
                                        'Receipts':receipts})
                                        
                            if tschol > 0:
                                feeinfo.append({'Type':'Scholarship', 'Amount':tschol, 'Total':'-',
                                                     'Balance':'-'})
                            if tspecialfee > 0:
                                feeinfo.append({'Type':'SpecialFee', 'Amount':tspecialfee, 'Total':'-',
                                                     'Balance':'-'})

                            specialfeeqs = ScholarshipOrFee.objects.filter(StudentYearlyInformation=data).filter(Type=2)
                            if specialfeeqs:
                                for specialfee in specialfeeqs:
                                    ftype = specialfee.FeeType
                                    amount = specialfee.Amount
                                    total = 0
                                    feereceipts = FeeReceipt.objects.filter(StudentYearlyInformation=data).filter(FeeType=ftype).filter(Status=1)
                                    feedateamount = []
                                    total = 0
                                    if feereceipts:
                                        for fr in feereceipts:
                                            feedateamount.append({'ReceiptNo':fr.ReceiptNumber, 'Date':fr.Date, 'Amount':fr.Amount})
                                            total += fr.Amount
                                    balance = amount - total
                                    if balance > 0:
                                        defaulter = 1
                                        style_opentag = STYLE_OPEN_TAG
                                        style_closetag = STYLE_CLOSE_TAG
                                        fstyle_opentag = STYLE_OPEN_TAG
                                        fstyle_closetag = STYLE_CLOSE_TAG
                                    feeinfo.append({'Type':ftype.Type, 'Amount':amount, 'FeeDateAmount': feedateamount, 'Total':total,
                                        'Balance':balance, 'FStyleOpenTag':fstyle_opentag, 'FStyleCloseTag':fstyle_closetag})

                            if show == '1' or defaulter == 1:
                                students.append({'Student':data.StudentBasicInfo, 'FeeInfo': feeinfo,
                                'YearlyInfo':data, 'StyleOpenTag':style_opentag, 'StyleCloseTag':style_closetag})

                if studentsfound:
                    return render_to_response('fees/feereport.html', {'form': form, 'message': message, 'students':students,
                                            'classmaster': cms[0] })
                else:
                    message = "No student records found!"
                    return render_to_response('fees/feereport.html', {'form': form, 'message': message})
        else:
            return render_to_response('fees/feereport.html', {'form': form, 'message': message})
        
#
def fee_collection(request):
    message = ""
    if not request.POST:
        form = FeeCollectionForm()
        return render_to_response('fees/feecollection.html', {'form': form, 'message': message})
    else:
        form = FeeCollectionForm(request.POST)
        if not form.is_valid():
            return render_to_response('fees/feecollection.html', {'form': form, 'message': message})
        
        date = form.cleaned_data['Date']
        frs = FeeReceipt.objects.filter(Date=date).filter(Status=1)
        if frs:
            feereceipts = []
            totalcash = 0
            totalcheque = 0
            for fr in frs:
                if fr.ChequeNo:
                    feereceipts.append({'receipt':fr, 'payment':fr.ChequeNo})
                    totalcheque += fr.Amount
                else:
                    feereceipts.append({'receipt':fr, 'payment':'Cash'})
                    totalcash += fr.Amount
            return render_to_response('fees/feecollection.html', {'form': form, 'message': message, 'receipts':feereceipts, 'date':date, 'totalcash':totalcash, 'totalcheque':totalcheque, 'grandtotal':totalcash + totalcheque})
        else:
            message = "No fee receipts for given date"
            return render_to_response('fees/feecollection.html', {'form': form, 'message': message})


#
def reprint_receipt(request):
    if request.POST:
        receiptno = request.POST['receiptno']
        fr = FeeReceipt.objects.filter(ReceiptNumber=receiptno)
        if fr:
            feerct = fr[0]
            return print_receipt(feerct)
    
    return HttpResponse ('<html><body></body></html>')

#
def print_receipt(feerct):
    student = feerct.StudentYearlyInformation.StudentBasicInfo
    id = feerct.ReceiptNumber
    date = feerct.Date
    std = feerct.StudentYearlyInformation.ClassMaster.Standard
    year = str(feerct.StudentYearlyInformation.ClassMaster.AcademicYear)
    amount = feerct.Amount
    feetype = feerct.FeeType.Type
    cheque = feerct.ChequeNo
    bank = feerct.Bank
    
    response = HttpResponse(mimetype='application/pdf')
    doc = SimpleDocTemplate(response,
                bottomMargin=0,
                topMargin=0,
                leftMargin=1.2*inch,
                rightMargin=0.8*inch)
                
    Story = []
    Story.append(Spacer(1,1*inch))

    ptable_style = TableStyle([
        ('FONT', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE',(0,0),(-1,-1),12)])

    rstable_style = TableStyle([
        ('FONT', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('ALIGN',(0,0),(-1,-1),'LEFT')])

    feetable_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Roman'),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('INNERGRID',(0,0),(-2,-3),0.25,colors.black),
        ('INNERGRID',(1,0),(-1,-3),0.25,colors.black),
        ('INNERGRID',(0,2),(-2,-1),0.25,colors.black),
        ('INNERGRID',(1,2),(-1,-1),0.25,colors.black),
        ('BOX',(0,0),(-1,-1),0.25,colors.black)])

    rsdata = []
    rscolwidth = (2*inch,2.5*inch,1.5*inch)
    rsdata.append(['Registration No: ' + str(student.RegistrationNo),'','Date: ' + date.strftime("%d-%m-%Y")])
    rsdata.append(['Name: ' + student.FirstName + ' ' + student.LastName,'','Receipt No: ' + str(id)])
    rsdata.append(['Standard: ' + str(std),'',''])
    rsdata.append(['Year: ' + year,'',''])
    
    rstable=Table(rsdata,colWidths=rscolwidth)
    rstable.setStyle(rstable_style);
    rstable.hAlign='LEFT'
    Story.append(rstable)

    if amount < 0:
        amount = -amount
        paid = "RECEIVED"
    else:
        paid = "PAID"

    fdata = []
    fdata.append(['Fee Type','Amount'])
    fdata.append([feetype,str(amount)])
    fdata.append(['',''])
    fdata.append(['Total', str(amount)])
    fcolwidth = (4*margin,4*margin)
    ftable=Table(fdata, colWidths=fcolwidth)
    ftable.setStyle(feetable_style);
    ftable.hAlign='CENTER'
    Story.append(ftable)
    Story.append(Spacer(1,0.2*inch))

    pdata = []
    n2w = Num2Word_EN()
    words = n2w.to_cardinal(amount)
    pdata.append(['In words:', words + " only", '', ''])                
    if cheque:
        pdata.append(['Payment Details:',paid, "By Cheque",''])
        pdata.append(['', "Cheque No: ", str(cheque),''])
        pdata.append(['', "Bank: ", bank,''])
    else:
        pdata.append(['Payment Details:',paid, "By Cash",''])
        pdata.append(['', "Cheque No: ", 'Nil',''])
        pdata.append(['', "Bank: ", 'Nil',''])
                
    ptable=Table(pdata)
    ptable.setStyle(ptable_style);
    ptable.hAlign='LEFT'
    Story.append(ptable)
    Story.append(Spacer(1,0.8*inch))
                
    addSignatureSpaceToStory(Story);

    Story.append(Spacer(1,1.5*inch))
    Story.append(rstable)
    Story.append(ftable)
    Story.append(Spacer(1,0.2*inch))
    Story.append(ptable)
    Story.append(Spacer(1,0.8*inch))
    addSignatureSpaceToStory(Story);

    doc.build(Story, onFirstPage=firstPage)
    return response

def addSignatureSpaceToStory(Story):
    stable_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    sealsign = []
    sealsign.append(['Seal','Signature'])
    colwidth = ((PAGE_WIDTH - 4*margin)/2,(PAGE_WIDTH - 4*margin)/2)
    table = Table(sealsign, colWidths=colwidth)
    table.setStyle(stable_style)
    Story.append(table)

def firstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-50, "Jnana Prabodhini Prashala")
    canvas.setFont('Times-Roman',8)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-60, "510 Sadashiv Peth Pune 411030")
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-70, "email: prashala@jnanaprabodhini.org")
    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH-rmargin-1*inch, PAGE_HEIGHT-45, "Office Copy")

    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, (PAGE_HEIGHT/2)-50, "Jnana Prabodhini Prashala")
    canvas.setFont('Times-Roman',8)
    canvas.drawCentredString(PAGE_WIDTH/2.0, (PAGE_HEIGHT/2)-60, "510 Sadashiv Peth Pune 411030")
    canvas.drawCentredString(PAGE_WIDTH/2.0, (PAGE_HEIGHT/2)-70, "email: prashala@jnanaprabodhini.org")
    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH-rmargin-1*inch, (PAGE_HEIGHT/2)-45, "Student Copy")

    canvas.restoreState()
    pageBorder(canvas)

def pageBorder(canvas):
    
    canvas.line(lmargin, tbmargin, lmargin, (PAGE_HEIGHT/2) - margin)
    canvas.line(lmargin, (PAGE_HEIGHT/2) - margin, PAGE_WIDTH - rmargin, (PAGE_HEIGHT/2) - margin)
    canvas.line(PAGE_WIDTH - rmargin, (PAGE_HEIGHT/2) - margin, PAGE_WIDTH - rmargin, tbmargin)
    canvas.line(PAGE_WIDTH - rmargin, tbmargin, lmargin, tbmargin)

    canvas.line(lmargin, margin + (PAGE_HEIGHT/2), lmargin, PAGE_HEIGHT - margin)
    canvas.line(lmargin, PAGE_HEIGHT - margin, PAGE_WIDTH - rmargin, PAGE_HEIGHT - margin)
    canvas.line(PAGE_WIDTH - rmargin,  PAGE_HEIGHT - margin, PAGE_WIDTH - rmargin, (PAGE_HEIGHT/2) + margin)
    canvas.line(PAGE_WIDTH - rmargin, (PAGE_HEIGHT/2) + margin, lmargin, margin + (PAGE_HEIGHT/2))


fee_receipt = login_required(fee_receipt)
fee_report = login_required(fee_report)
reprint_receipt = login_required(reprint_receipt)
fee_collection = login_required(fee_collection)
