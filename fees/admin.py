from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from jp_sms.fees.models import FeeType, FeeReceipt
import datetime

class feetypeAdmin(admin.ModelAdmin):
    list_display = ('ClassMaster','Type','Amount')
    ordering = ('ClassMaster',)
    list_filter = ['ClassMaster','Type']
    search_fields = ['ClassMaster__AcademicYear__Year', 'ClassMaster__Standard', 'ClassMaster__Division', 'ClassMaster__Teacher__Name' ]
    pass
				
class feereceiptAdmin(admin.ModelAdmin):
    list_display = ('ReceiptNumber','Date','StudentYearlyInformation','FeeType','Amount')
    ordering = ('ReceiptNumber',)
    list_filter = ['FeeType','StudentYearlyInformation']
    search_fields = ['ReceiptNumber', 'StudentYearlyInformation__StudentBasicInfo__FirstName', 'StudentYearlyInformation__StudentBasicInfo__RegistrationNo']
    pass

admin.site.register(FeeType, feetypeAdmin)
admin.site.register(FeeReceipt, feereceiptAdmin)
