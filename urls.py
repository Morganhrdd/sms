from django.conf.urls.defaults import *
#from students import views
# The next two lines enable the admin and load each admin.py file:
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/ams/home/', 'ams.views.admin_home'),
    (r'^admin/(.*)', admin.site.root),
    (r'^marks_add/', 'students.views.marks_add'),
    (r'^attendance_add/', 'students.views.attendance_add'),
    (r'^report/', 'students.views.report'),
    (r'^ams/', 'ams.views.get_barcode'),
    (r'^leave/', 'ams.views.app_leave'),
    (r'^ams_report/', 'ams.views.monthly_report'),
    (r'^ams_daily_report/', 'ams.views.daily_report'),
    (r'^ams_display/', 'ams.views.ams_display'),
    (r'^fee/', 'fees.views.fee_receipt'),
    (r'^fee_receipt/', 'fees.views.reprint_receipt'),
    (r'^fee_report/', 'fees.views.fee_report'),
    (r'^reportPDF/', 'students.views.reportPDF'),
    (r'^certificatePDF/', 'students.views.certificatePDF'),
    (r'^schoolLeavingPDF/', 'students.views.schoolLeavingPDF'),
    (r'^fee_collection/', 'fees.views.fee_collection'),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^ams_dayrules/', 'ams.views.add_dayrules'),
    ##(r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^$', direct_to_template,  { 'template': 'index.html' }, 'index'),
    (r'^pravesh/add', 'pravesh.views.add'),
    (r'^pravesh/hallticket/(\d+)/?$','pravesh.views.display_hallticket'),
    (r'^pravesh/hallticket/(\d+)/edit/?$','pravesh.views.edit'),
    #(r'^pravesh/edit/(\d+)/?', 'pravesh.views.edit'),
    (r'^pravesh/generate_hallticket','pravesh.views.generate_hallticket'),
    (r'^pravesh/?','pravesh.views.index'),
    #(r'^useradd/', views.user_add),
    # ... the rest of your URLs here ...
)
