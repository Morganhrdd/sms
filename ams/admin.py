from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from jp_sms.ams.models import Category, User, UserStatus, TimeRules, DayRules, Attendance, TimeRecords, ForgotCheckout
from jp_sms.ams.models import Leaves, LeaveRules, AcademicYear, LeaveAttendance, LeavesBalance, EncashLeaves, Overtime
import datetime

class categoryAdmin(admin.ModelAdmin):
	list_display = ('Description','Id',)
	ordering = ('Id',)
	search_fields =['Description']
	pass
	
class userAdmin(admin.ModelAdmin):
	list_display = ('Name','Barcode','Category',)
	ordering = ('Barcode',)
	search_fields =['Barcode', 'Name']
	def save_model(self, request, obj, form, change):
		if not change:
			userstatus = UserStatus()
			userstatus.Barcode = obj
			userstatus.Status = 'O'
			userstatus.save()
		obj.save()
			
class userstatusAdmin(admin.ModelAdmin):
	list_display = ('Barcode','Status')
	ordering = ('Barcode',)
	search_fields = ['Barcode__Barcode']
	pass
		
class timerulesAdmin(admin.ModelAdmin):
	list_display = ('Type','TimeIn','LateIn','HalfIn','HalfOut','EarlyOut','TimeOut',)
	ordering = ('Type',)
	search_fields =['Type',]
	pass
	
class dayrulesAdmin(admin.ModelAdmin):
	list_display = ('Category','Barcode','Day','Date','Type')
	ordering = ('Category','Date','Day')
	search_fields =['Type__Type']
	pass
	
class attendanceAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'Date', 'Remark', 'Comment')
	ordering = ('Barcode', 'Date')
	search_fields = ['Barcode__Barcode', ]
	list_filter = ['Year', 'Barcode']
	pass

class timerecordsAdmin(admin.ModelAdmin):
	list_display = ('Barcode','Type','Date','Time')
	ordering = ('Barcode',)
	search_fields = ['Date', 'Barcode__Barcode']
	list_filter = ['Barcode', 'Date']
	def save_model(self, request, obj, form, change):
		if obj.Type == 'O':
			fcr = ForgotCheckout.objects.filter(Barcode=obj.Barcode).filter(Date=obj.Date)
			if fcr:
				fcr[0].Status = 2
				fcr[0].save()
		obj.save()
	pass
	
class leavesAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'ApplicationDate', 'LeaveDate', 'Type', 'Status')
	ordering = ('Barcode',)
	search_fields = ['Barcode__Barcode', 'LeaveDate']
	list_filter = ['LeaveDate', 'Status']

	def save_model(self, request, obj, form, change):
		if change:
			dt = datetime.datetime.now()
			obj.ApprovalDate = dt.date()
			if obj.Status == 2:
				prevatt = Attendance.objects.filter(Date=obj.LeaveDate).filter(Barcode=obj.Barcode)
				if prevatt:
					attendance = prevatt[0]
				else:
					attendance = LeaveAttendance()
					attendance.Barcode = obj.Barcode
					attendance.Date = obj.LeaveDate

				if obj.Type == 4:
					attendance.Remark = 'D'
				elif obj.Type == 5:
					attendance.Remark = 'F'
				else:
					attendance.Remark = 'O'
				attendance.save()
			else:
				att = LeaveAttendance.objects.filter(Date=obj.LeaveDate).filter(Barcode=obj.Barcode)
				att[0].delete()
		obj.save()
		
	pass
	
class leaverulesAdmin(admin.ModelAdmin):
	list_display = ('Category', 'Type', 'Days')
	ordering = ('Category',)
	search_fields = ['Category__Id']
#	list_filter = ['Category__Description']
	pass

class academicyearAdmin(admin.ModelAdmin):
	list_display = ('Title', 'StartDate', 'EndDate', 'Status')
	ordering = ('Title',)
	search_fields = ['Status', 'Title']

	def save_model(self, request, obj, form, change):
		if obj.Status == 1:
			years = AcademicYear.objects.filter(Status=1)
			if years and (years[0] != obj):
				obj.Status = 2
		obj.save()
	pass
	
class leavesbalanceAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'Type', 'Days')
	ordering = ('Barcode',)
	list_filter = ['Barcode']
	pass

class encashleavesAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'Days', 'Status')
	ordering = ('Barcode',)
	list_filter = ['Barcode', 'Status']
	pass

class overtimeAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'Date', 'Hours', 'Status')
	ordering = ('Barcode',)
	list_filter = ['Barcode', 'Status']
	def save_model(self, request, obj, form, change):
		if change and (obj.Status == 2 or obj.Status == 3):
			dt = datetime.datetime.now()
			obj.ApprovalDate = dt.date()
		obj.save()
	pass

class forgotcheckoutAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'Date', 'Status')
	ordering = ('Barcode',)
	list_filter = ['Barcode', 'Date', 'Status']
	pass
	
admin.site.register(Category, categoryAdmin)
admin.site.register(User, userAdmin)
admin.site.register(UserStatus, userstatusAdmin)
admin.site.register(TimeRules, timerulesAdmin)
admin.site.register(DayRules, dayrulesAdmin)
admin.site.register(Attendance, attendanceAdmin)
admin.site.register(TimeRecords, timerecordsAdmin)
admin.site.register(Leaves, leavesAdmin)
admin.site.register(LeaveRules, leaverulesAdmin)
admin.site.register(AcademicYear, academicyearAdmin)
admin.site.register(LeavesBalance, leavesbalanceAdmin)
admin.site.register(EncashLeaves, encashleavesAdmin)
admin.site.register(Overtime, overtimeAdmin)
admin.site.register(ForgotCheckout, forgotcheckoutAdmin)
