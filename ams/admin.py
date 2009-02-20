from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from jp_sms.ams.models import Category, User, UserStatus, TimeRules, DayRules, Attendance, TimeRecords, Leaves, LeaveRules, AcademicYear

class categoryAdmin(admin.ModelAdmin):
	list_display = ('Description','Id',)
	ordering = ('Id',)
	search_fields =['Description']
	pass
	
class userAdmin(admin.ModelAdmin):
	list_display = ('Name','Barcode','Category',)
	ordering = ('Barcode',)
	search_fields =['Barcode', 'Name']
	pass

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
	pass
	
class leavesAdmin(admin.ModelAdmin):
	list_display = ('Barcode', 'ApplicationDate', 'LeaveDate', 'Type', 'Status')
	ordering = ('Barcode',)
	search_fields = ['Barcode__Barcode', 'LeaveDate']

	def save_model(self, request, obj, form, change):
		if change:
			if obj.Status == 2:
				prevatt = Attendance.objects.filter(Date=obj.LeaveDate).filter(Barcode=obj.Barcode)
				if prevatt:
					attendance = prevatt[0]
				else:
					attendance = Attendance()
					attendance.Barcode = obj.Barcode
					attendance.Date = obj.LeaveDate
					attendance.Year = AcademicYear.objects.filter(Status=1)[0]
				attendance.Remark = 'O'
				attendance.save()
		obj.save()
		
	pass
	
class leaverulesAdmin(admin.ModelAdmin):
	list_display = ('Category', 'Type', 'Days')
	ordering = ('Category',)
	search_fields = ['Category__Id']
	pass

class academicyearAdmin(admin.ModelAdmin):
	list_display = ('Title', 'StartDate', 'EndDate', 'Status')
	ordering = ('Title',)
	search_fields = ['Status', 'Title']

	def save_model(self, request, obj, form, change):
		if obj.Status == 1:
			years = AcademicYear.objects.filter(Status=1)
			if years:
				obj.Status = 2
		obj.save()
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