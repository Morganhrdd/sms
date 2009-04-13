# Create your views here.

from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponse 
from django.template import Context
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

from jp_sms.fees.models import StudentBasicInfo, AcademicYear, ClassMaster, StudentYearlyInformation
from jp_sms.fees.models import FeeType, FeeReceipt
from jp_sms.fees.models import FeeForm

from jp_sms.fees.num2word_EN import Num2Word_EN

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
				
				response = HttpResponse(mimetype='application/pdf')
				doc = SimpleDocTemplate(response,
								bottomMargin=0,
								topMargin=0)
				
				Story = []
				Story.append(Spacer(1,1*inch))

				table_style = TableStyle([
					('FONT', (0,0), (-1,0), 'Times-Roman'),
					('FONTSIZE',(0,0),(-1,-1),8)])

				table_style1 = TableStyle([
					('FONT', (0,0), (-1,0), 'Times-Roman'),
					('FONTSIZE',(0,0),(-1,-1),8),
					('ALIGN',(0,0),(-1,-1),'CENTER')])

				rdata = []
				rdata = (
					['Date: ' + date.strftime("%d-%m-%Y")],
					['Receipt No: ' + str(id)])
				rtable=Table(rdata)
				rtable.setStyle(table_style);
				rtable.hAlign='RIGHT'
				Story.append(rtable)

				studentdata = []
				studentdata=(
					['Registration No: ' + str(student.RegistrationNo)],
					['Name: ' + student.FirstName + ' ' + student.LastName],
					['Standard: ' + str(std)],
					['Year: ' + year])
				studenttable=Table(studentdata)
				studenttable.setStyle(table_style);
				studenttable.hAlign='LEFT'
				Story.append(studenttable)
				
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
				fcolwidth = (10*margin,10*margin)
				ftable=Table(fdata, colWidths=fcolwidth)
				ftable.setStyle(table_style1);
				ftable.hAlign='CENTER'
				Story.append(ftable)
				#Story.append(Spacer(1,0.5*inch))

				pdata = []
				n2w = Num2Word_EN()
				words = n2w.to_cardinal(amount)
				pdata.append(['In words', words])				
				pdata.append(['Payment Details:',paid])
				if cheque:
					pdata.append(["Cheque No. :",str(cheque)])
					pdata.append(["Bank: ", bank])
				else:
					pdata.append(["By Cash",''])
					pdata.append(['', ''])
				
				ptable=Table(pdata)
				ptable.setStyle(table_style);
				ptable.hAlign='LEFT'
				Story.append(ptable)
				Story.append(Spacer(1,0.6*inch))
				
				addSignatureSpaceToStory(Story);

				Story.append(Spacer(1,1.5*inch))
				Story.append(rtable)
				Story.append(studenttable)
				Story.append(ftable)
				Story.append(ptable)
				Story.append(Spacer(1,0.6*inch))
				addSignatureSpaceToStory(Story);

				doc.build(Story, onFirstPage=firstPage)
				return response
				
#				return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,'receiptnumber':receiptnumber })					

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
						hostel = data.Hostel
						if hostel == 
						feetypes = FeeType.objects.filter(ClassMaster=data.ClassMaster)
						feeinfo = []
						if feetypes:
							for ftype in feetypes:
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
								feeinfo.append({'Type':ftype.Type, 'Amount':ftype.Amount, 'FeeDateAmount': feedateamount, 'Total':total,
												 'Balance':amount - total})
						years.append({'ClassMaster':data.ClassMaster, 'FeeInfo': feeinfo})															

				return render_to_response('fees/feeform.html', {'form': form, 'message': message, 'date':date,
											'receiptnumber':receiptnumber, 'student':student, 'years':years })					

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
margin=0.2*inch

def addSignatureSpaceToStory(Story):
	table_style1 = TableStyle([
		('ALIGN',(0,0),(-1,-1),'CENTER')])
	sealsign = []
	sealsign.append(['Seal','Signature'])
	colwidth = ((PAGE_WIDTH - 4*margin)/2,(PAGE_WIDTH - 4*margin)/2)
	table = Table(sealsign, colWidths=colwidth)
	table.setStyle(table_style1)
	Story.append(table)

def firstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-40, "Jnana Prabodhini Prashala")
    canvas.setFont('Times-Roman',8)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-50, "510 Sadashiv Peth Pune 411030")
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-60, "email: prashala@jnanaprabodhini.org")
    #canvas.setFont('Times-Roman',9)
    #canvas.drawString(inch, 0.75 * inch, "%s, Page %d" % (pageinfo, doc.page))
    #margin=0.7*inch
    #canvas.line(PAGE_HEIGHT-145, (margin * 1.2), PAGE_HEIGHT-145, PAGE_WIDTH - (margin * 1.2))

    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, (PAGE_HEIGHT/2)-40, "Jnana Prabodhini Prashala")
    canvas.setFont('Times-Roman',8)
    canvas.drawCentredString(PAGE_WIDTH/2.0, (PAGE_HEIGHT/2)-50, "510 Sadashiv Peth Pune 411030")
    canvas.drawCentredString(PAGE_WIDTH/2.0, (PAGE_HEIGHT/2)-60, "email: prashala@jnanaprabodhini.org")

    canvas.restoreState()
    pageBorder(canvas)

def pageBorder(canvas):
    
    canvas.line(margin, margin, margin, (PAGE_HEIGHT/2) - margin)
    canvas.line(margin, (PAGE_HEIGHT/2) - margin, PAGE_WIDTH - margin, (PAGE_HEIGHT/2) - margin)
    canvas.line(PAGE_WIDTH - margin, (PAGE_HEIGHT/2) - margin, PAGE_WIDTH - margin, margin)
    canvas.line(PAGE_WIDTH - margin, margin, margin, margin)

    canvas.line(margin, margin + (PAGE_HEIGHT/2), margin, PAGE_HEIGHT - margin)
    canvas.line(margin, PAGE_HEIGHT - margin, PAGE_WIDTH - margin, PAGE_HEIGHT - margin)
    canvas.line(PAGE_WIDTH - margin,  PAGE_HEIGHT - margin, PAGE_WIDTH - margin, (PAGE_HEIGHT/2) + margin)
    canvas.line(PAGE_WIDTH - margin, (PAGE_HEIGHT/2) + margin, margin, margin + (PAGE_HEIGHT/2))

def laterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch, "%s, Page %d" % (pageinfo, doc.page))
    canvas.restoreState()
    pageBorder(canvas)

def reportPDF(request):
    #for param in os.environ.keys():
    #    print "%20s %s" % (param,os.environ[param])
    #return HttpResponse()
    #if request.GET.has_key('id'):
        response = HttpResponse(mimetype='application/pdf')
        doc = SimpleDocTemplate(response)

        student_yearly_info = StudentYearlyInformation.objects.get(id=1)
        
        Story = []
        fillStaticAndYearlyInfo(student_yearly_info, Story)
        fillAcademicReport(student_yearly_info, Story)
        fillCoCurricularReport(student_yearly_info, Story)
        fillOutdoorActivityReport(student_yearly_info, Story)
        #fillLibraryReport(student_yearly_info, Story)
        doc.build(Story, onFirstPage=firstPage, onLaterPages=laterPages)
        return response
    #else:
    #    return HttpResponse('Id not provided')
						