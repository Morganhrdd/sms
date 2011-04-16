from reportlab.lib.units import inch
from sms.students.models import STANDARD_CHOICES
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import getSampleStyleSheet

RECEIPT_CHOICES = (
    (1, 'Valid'),
    (2, 'Cancel'),
)

FEE_FILTER_CHOICES = (
	(1, 'All'),
	(2, 'Defaulters')
)

FEE_DIVISION_CHOICES = (
    ('A', 'All'),
    ('G', 'Girls'),
    ('B', 'Boys'),
)

FEE_CHOICES = (
	(1, 'Scholarship'),
	(2, 'Special Fee'),
)


PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
#PAGE_HEIGHT=8*inch; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
margin=0.4*inch
tbmargin=0.5*inch
rmargin=0.8*inch
lmargin=1.2*inch

