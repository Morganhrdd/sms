from jp_sms.pravesh.models import DateTimeDetails, ClassRoom, Session, Student, HallTicket
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class DateTimeDetailsAdmin(admin.ModelAdmin):
    list_display = ['Start', 'End']

class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['Number', 'Medium', 'Name', 'Capacity']
    search_fields = ['Number', 'Medium', 'Name', 'Capacity']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['Number', 'Name', 'DateTimeDetails']
    search_fields = ['Number', 'Name', 'DateTimeDetails']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['FirstName', 'LastName', 'Email', 'Gender']
    search_fields = ['FirstName', 'LastName', 'Email', 'Gender']

class HallTicketAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(DateTimeDetails, DateTimeDetailsAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(HallTicket, HallTicketAdmin)
